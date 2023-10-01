from wpilib import XboxController
from wpimath import applyDeadband
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_STRAFE_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_ROTATE_SPEED_RAD_PER_SEC
from utils.faults import Fault
from utils.signalLogging import log



class DriverInterface():

    def __init__(self):
        ctrlIdx = 0
        self.ctrl = XboxController(ctrlIdx)
        self.fwdRevCmd = 0
        self.strafeCmd = 0
        self.rotateCmd = 0
        self.connectedFault = Fault(f"Driver XBox Controller ({ctrlIdx}) Unplugged")



    def update(self):
        
        if(self.ctrl.isConnected()):
            fwdRevJoy = applyDeadband(self.ctrl.getLeftX(),0.1)
            strafeJoy = applyDeadband(self.ctrl.getLeftY(),0.1)
            rotateJoy = applyDeadband(self.ctrl.getRightX(),0.1)

            self.fwdRevCmd = fwdRevJoy * -1.0 * MAX_FWD_REV_SPEED_MPS
            self.strafeCmd = strafeJoy * -1.0 * MAX_STRAFE_SPEED_MPS
            self.rotateCmd = rotateJoy * -1.0 * MAX_ROTATE_SPEED_RAD_PER_SEC
            self.connectedFault.setNoFault()
        else:
            self.fwdRevCmd = 0.0
            self.strafeCmd = 0.0
            self.rotateCmd = 0.0
            self.connectedFault.setFaulted()

        log("DI FwdRev Cmd", self.fwdRevCmd, "mps")
        log("DI Strafe Cmd", self.strafeCmd, "mps")
        log("DI Rotate Cmd", self.rotateCmd, "radPerSec")
        log("DI connected", self.ctrl.isConnected(), "bool")

    def getFwdRevCmd(self):
        return self.fwdRevCmd

    def getStrafeCmd(self):
        return self.strafeCmd
    
    def getRotateCmd(self):
        return self.rotateCmd
