
import os
import logging
from datetime import  datetime
import wpilib

class CrashLogger():

    def update(self):
        if(not self.prefixWritten and wpilib.DriverStation.isFMSAttached()):

            self.logPrint(f"==========================================")
            self.logPrint(f"== FMS Data Received {datetime.now()}:")
            self.logPrint(f"Event: {wpilib.DriverStation.getEventName()}")
            self.logPrint(f"Match Type: {wpilib.DriverStation.getMatchType()}")
            self.logPrint(f"Match Number: {wpilib.DriverStation.getMatchNumber()}")
            self.logPrint(f"Replay Number: {wpilib.DriverStation.getReplayNumber()}")
            self.logPrint(f"Game Message: {wpilib.DriverStation.getGameSpecificMessage()}")
            self.logPrint(f"Cur FPGA Time: {wpilib.Timer.getFPGATimestamp()}")
            self.logPrint(f"==========================================")
            self.prefixWritten = True

    def logPrint(self, msg):
        self.fileHandler.stream.write(msg)
        self.fileHandler.stream.write("\n")
        self.fileHandler.stream.flush()

    def __init__(self):

        self.prefixWritten = False

        # Pick the output folder and make it at install time to make sure 
        # it's there, just in case a crash happens later
        if wpilib.RobotBase.isSimulation():
            logDir = "./simulationCrashLogs"
        else:
            logDir = "/U/crashLogs"

        if(not os.path.isdir(logDir)):
            os.makedirs(logDir)

        # Iterate till we got a unique log name
        idx=0
        uniqueFileFound = False
        logPath = ""
        while(not uniqueFileFound):
            logFileName = f"crashLog_{idx}.txt"
            logPath = os.path.join(logDir, logFileName)
            uniqueFileFound = not os.path.isfile(logPath)
            idx += 1

        # Install a custom logger for all errors. This shoudl include stacktraces
        # if the robot crashes on the field.
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()

        self.fileHandler = logging.FileHandler(logPath)
        self.fileHandler.setFormatter(logFormatter)
        self.fileHandler.setLevel(logging.ERROR)
        rootLogger.addHandler(self.fileHandler)

        self.logPrint(f"\n==============================================")
        self.logPrint(f"Beginning of Log {logPath}")
        self.logPrint(f"Started {datetime.now()}")
