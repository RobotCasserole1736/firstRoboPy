from wpimath.kinematics import ChassisSpeeds
from wpimath.geometry import Pose2d

from utils.signalLogging import log
from drivetrain.swerveModuleControl import SwerveModuleControl
from drivetrain.drivetrainPhysical import FL_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import FR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BL_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import kinematics

class DrivetrainControl():
    def __init__(self):
        self.modules = []
        self.modules.append(SwerveModuleControl("FL", 0, 1, 0, FL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("FR", 2, 3, 1, FR_ENCODER_MOUNT_OFFSET_RAD, True))
        self.modules.append(SwerveModuleControl("BL", 4, 5, 2, BL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("BR", 6, 7, 3, BR_ENCODER_MOUNT_OFFSET_RAD, True))
        
        self.desChSpd = ChassisSpeeds()
        self.curDesPose = Pose2d()
    
    def setCmdBrace(self):
        pass # TODO

    def setCmdFieldRelative(self, downUpFieldCmd, leftRightFieldCmd, rotateCmd):
        pass # TODO

    def setCmdRobotRelative(self, fwdRevCmd, strafeCmd, rotateCmd):
        self.desChSpd = ChassisSpeeds(fwdRevCmd, strafeCmd, rotateCmd)


    def update(self):
        desModStates = kinematics.toSwerveModuleStates(self.desChSpd)

        for idx, module in enumerate(self.modules):
            module.setDesiredState(desModStates[idx])
            module.update()
