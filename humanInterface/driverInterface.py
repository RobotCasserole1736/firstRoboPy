from wpilib import XboxController
from wpimath import applyDeadband
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_STRAFE_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_ROTATE_SPEED_RAD_PER_SEC
from utils.faults import Fault
from utils.signalLogging import log



class DriverInterface():
    """Class to gather input from the driver of the robot 
    """

    def __init__(self):
        ctrlIdx = 0
        self.ctrl = XboxController(ctrlIdx)
        self.velXCmd = 0
        self.velYCmd = 0
        self.velTCmd = 0
        self.connectedFault = Fault(f"Driver XBox Controller ({ctrlIdx}) Unplugged")

    def update(self):
        """Main update - call this once every 20ms
        """
        
        if(self.ctrl.isConnected()):
            # Only attempt to read from the joystick if it's plugged in
            vXJoy = applyDeadband(self.ctrl.getLeftX(),0.1)
            vYJoy = applyDeadband(self.ctrl.getLeftY(),0.1)
            vTJoy = applyDeadband(self.ctrl.getRightX(),0.1)

            self.velXCmd = vXJoy * -1.0 * MAX_FWD_REV_SPEED_MPS
            self.velYCmd = vYJoy * -1.0 * MAX_STRAFE_SPEED_MPS
            self.velTCmd = vTJoy * -1.0 * MAX_ROTATE_SPEED_RAD_PER_SEC
            self.connectedFault.setNoFault()
        else:
            # If the joystick is unplugged, pick safe-state commands and raise a fault
            self.velXCmd = 0.0
            self.velYCmd = 0.0
            self.velTCmd = 0.0
            self.connectedFault.setFaulted()

        log("DI FwdRev Cmd", self.velXCmd, "mps")
        log("DI Strafe Cmd", self.velYCmd, "mps")
        log("DI Rotate Cmd", self.velTCmd, "radPerSec")
        log("DI connected", self.ctrl.isConnected(), "bool")

    def getVxCmd(self):
        """
        Returns:
            float: Driver's current vX (downfield/upfield, or fwd/rev) command in meters per second
        """
        return self.velXCmd

    def getVyCmd(self):
        """
        Returns:
            float: Driver's current vY (side-to-side or strafe) command in meters per second
        """
        return self.velYCmd
    
    def getVtCmd(self):
        """
        Returns:
            float: Driver's current vT (rotation) command in radians per second
        """
        return self.velTCmd
