from wpilib import XboxController
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_STRAFE_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_ROTATE_SPEED_RAD_PER_SEC


class DriverInterface():

    def __init__(self):
        self.ctrl = XboxController(0)
        self.fwdRevCmd = 0
        self.strafeCmd = 0
        self.rotateCmd = 0

    def update(self):
        self.fwdRevCmd = self.ctrl.getLeftX() * -1.0 * MAX_FWD_REV_SPEED_MPS
        self.strafeCmd = self.ctrl.getLeftY() * -1.0 * MAX_STRAFE_SPEED_MPS
        self.rotateCmd = self.ctrl.getLeftX() * -1.0 * MAX_ROTATE_SPEED_RAD_PER_SEC

    def getFwdRevCmd(self):
        return self.fwdRevCmd

    def getStrafeCmd(self):
        return self.strafeCmd
    
    def getRotateCmd(self):
        return self.rotateCmd
