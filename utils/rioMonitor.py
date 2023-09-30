from wpilib import RobotController
from utils.faults import Fault
from utils.signalLogging import log


# Records faults and runtime metrics for the roboRIO
class RIOMonitor():
    def __init__(self):
        self.railFault5v = Fault("RIO 5V (DIO) Rail Faulted")
        self.railFault3p3v = Fault("RIO 3.3V Rail Faulted")
        self.railFault6v = Fault("RIO 6V (PWM) Rail Faulted")

    def update(self):
        if(not RobotController.isBrownedOut()):
            self.railFault3p3v.set(not RobotController.getEnabled3V3())
            self.railFault5v.set(not RobotController.getEnabled5V())
            self.railFault6v.set(not RobotController.getEnabled6V())

        status = RobotController.getCANStatus()
        log("RIO CAN Bus Usage", status.percentBusUtilization, "pct")
        log("RIO CAN Bus Err Count", status.txFullCount + 
                                     status.receiveErrorCount + 
                                     status.transmitErrorCount, 
                                     "count")
        log("RIO Supply Voltage", RobotController.getInputVoltage(), "V")
