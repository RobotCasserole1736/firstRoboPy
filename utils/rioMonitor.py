import io
from threading import Thread
import time
import subprocess
from wpilib import RobotController
from wpilib import RobotBase
from utils.faults import Fault
from utils.signalLogging import log


# Records faults and runtime metrics for the roboRIO
class RIOMonitor:
    def __init__(self):
        self.railFault5v = Fault("RIO 5V (DIO) Rail Faulted")
        self.railFault3p3v = Fault("RIO 3.3V Rail Faulted")
        self.railFault6v = Fault("RIO 6V (PWM) Rail Faulted")

        # CPU Stats - remember last time metrics
        self.prevUserTime = 0
        self.prevNicedTime = 0
        self.prevSystemTime = 0
        self.prevIdleTime = 0

        self.thread1 = Thread(target=self._updateFast, daemon=True)
        self.thread2 = Thread(target=self._updateSlow, daemon=True)
        self.runCmd = True
        self.thread1.start()
        self.thread2.start()

    def stopThreads(self):
        self.runCmd = False
        self.thread1.join()
        self.thread2.join()

    # Things that should be recorded fairly quickly
    def _updateFast(self):
        while self.runCmd:
            self._updateVoltages()
            time.sleep(0.02)

    # Things that don't have to be updated as fast
    def _updateSlow(self):
        while self.runCmd:
            self._updateMemStats()
            self._updateCPUStats()
            self._updateCANStats()
            self._updateDiskStats()
            time.sleep(1.0)

    def _updateDiskStats(self):
        if RobotBase.isReal():
            # Use the built-in `df` command to get info about disk usage
            with subprocess.Popen("df", stdout=subprocess.PIPE) as result:
                if result.stdout is not None:
                    for line in io.TextIOWrapper(
                        result.stdout, encoding="utf-8"
                    ):  # abstract-class-instantiated: ignore
                        lineParts = line.split()
                        lineParts = [i for i in lineParts if i]
                        try:
                            mountDir = str(lineParts[5])
                            usedBytes = int(lineParts[2])
                            availBytes = int(lineParts[3])
                        except ValueError:
                            continue  # Skip this line if we couldn't parse values

                        pctUsed = usedBytes / float(usedBytes + availBytes) * 100.0
                        if mountDir == "/":
                            log("RIO SD Card Disk Usage", pctUsed, "pct")
                        elif mountDir.startswith("/media"):
                            mountDir = mountDir.replace("/", "\\")
                            log(f"RIO USB {mountDir} Disk Usage", pctUsed, "pct")

    def _updateCANStats(self):
        status = RobotController.getCANStatus()
        log("RIO CAN Bus Usage", status.percentBusUtilization, "pct")
        log(
            "RIO CAN Bus Err Count",
            status.txFullCount + status.receiveErrorCount + status.transmitErrorCount,
            "count",
        )

    def _updateVoltages(self):
        log("RIO Supply Voltage", RobotController.getInputVoltage(), "V")
        if not RobotController.isBrownedOut():
            self.railFault3p3v.set(not RobotController.getEnabled3V3())
            self.railFault5v.set(not RobotController.getEnabled5V())
            self.railFault6v.set(not RobotController.getEnabled6V())

    def _updateCPUStats(self):
        if RobotBase.isReal():
            curUserTime = 0
            curNicedTime = 0
            curSystemTime = 0
            curIdleTime = 0
            loadLine = None

            # The /proc/stat file contains running totals
            # of how long the CPU spent doing different things
            with open("/proc/stat", "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("cpu "):
                        loadLine = line
                        break

            if loadLine is not None:
                # Parse out the running totals
                parts = loadLine.split(" ")
                parts = [i for i in parts if i]  # Filter out empty strings
                try:
                    curUserTime = float(parts[1])
                    curNicedTime = float(parts[2])
                    curSystemTime = float(parts[3])
                    curIdleTime = float(parts[4])
                except ValueError:
                    return  # Skip this time if we couldn't parse out values

                # Calculate how much those totals changed from last time
                deltaUserTime = curUserTime - self.prevUserTime
                deltaNicedTime = curNicedTime - self.prevNicedTime
                deltaSystemTime = curSystemTime - self.prevSystemTime
                deltaIdleTime = curIdleTime - self.prevIdleTime

                # Add up how much time the CPU spent doing something useful
                totalInUseTime = deltaUserTime + deltaNicedTime + deltaSystemTime

                # Add up how much total time (in-use and idle together)
                totalTime = totalInUseTime + deltaIdleTime

                # Calculate and log  the Load Percent as percentage of
                # total time that we were not idle
                log("RIO CPU Load", totalInUseTime / totalTime * 100.0, "pct")

                # Remember current stats for next time
                self.prevUserTime = curUserTime
                self.prevNicedTime = curNicedTime
                self.prevSystemTime = curSystemTime
                self.prevIdleTime = curIdleTime

    def _updateMemStats(self):
        if RobotBase.isReal():
            memTotalStr = None
            memFreeStr = None

            # Read lines out of the special linux "meminfo" file
            with open("/proc/meminfo", "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("MemTotal:"):
                        memTotalStr = line
                    elif line.startswith("MemFree:"):
                        memFreeStr = line

            # If we found both lines, parse out the numbers we care about
            if memTotalStr is not None and memFreeStr is not None:
                memTotalParts = memTotalStr.split()
                memFreeParts = memFreeStr.split()

                try:
                    curTotalMem = float(memTotalParts[1])
                    curFreeMem = float(memFreeParts[1])
                except ValueError:
                    return  # Skip this time if we couldn't parse out values

                log("RIO Memory Usage", (1.0 - curFreeMem / curTotalMem) * 100.0, "pct")
