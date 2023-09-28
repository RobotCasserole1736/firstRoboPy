from wpimath.kinematics import ChassisSpeeds
from wpimath.geometry import Pose2d

from drivetrain.drivetrainPoseEstimator import DrivetrainPoseEstimator
from drivetrain.swerveModuleControl import SwerveModuleControl
from drivetrain.swerveModuleGainSet import SwerveModuleGainSet
from drivetrain.drivetrainTrajectoryControl import DrivetrainTrajectoryControl
from drivetrain.drivetrainPhysical import FL_ENCODER_MOUNT_OFFSET_RAD, MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import FR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BL_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import kinematics

class _DrivetrainControl():
    def __init__(self):
        self.modules = []
        self.modules.append(SwerveModuleControl("FL", 0, 1, 0, FL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("FR", 2, 3, 1, FR_ENCODER_MOUNT_OFFSET_RAD, True))
        self.modules.append(SwerveModuleControl("BL", 4, 5, 2, BL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("BR", 6, 7, 3, BR_ENCODER_MOUNT_OFFSET_RAD, True))
        
        self.desChSpd = ChassisSpeeds()
        self.curDesPose = Pose2d()

        self.gains = SwerveModuleGainSet()

        self.calUpdate(True)

        self.pe = DrivetrainPoseEstimator(self.getModulePositions())
        
        self.tc = DrivetrainTrajectoryControl()

    def calUpdate(self, force=False):
        if(self.gains.hasChanged() or force):
            for module in self.modules:
                module.setClosedLoopGains(self.gains)

    def setCmdFieldRelative(self, downUpFieldCmd, leftRightFieldCmd, rotateCmd):
        self.desChSpd = ChassisSpeeds.fromFieldRelativeSpeeds(downUpFieldCmd, leftRightFieldCmd, rotateCmd, self.pe.getCurEstPose().rotation())
        self.pe.setDesiredPose(self.pe.getCurEstPose())

    def setCmdRobotRelative(self, fwdRevCmd, strafeCmd, rotateCmd):
        self.desChSpd = ChassisSpeeds(fwdRevCmd, strafeCmd, rotateCmd)
        self.pe.setDesiredPose(self.pe.getCurEstPose())
        
    def setCmdTrajectory(self, cmd):
        self.desChSpd = self.tc.update(cmd, self.pe.getCurEstPose())
        self.pe.setDesiredPose(Pose2d(cmd.pose.translation(), cmd.holonomicRotation))


    def update(self):

        desModStates = kinematics.toSwerveModuleStates(self.desChSpd)
        kinematics.desaturateWheelSpeeds(desModStates, MAX_FWD_REV_SPEED_MPS)

        for idx, module in enumerate(self.modules):
            module.setDesiredState(desModStates[idx])
            module.update()
            
        self.pe.update(self.getModulePositions())

    def getModulePositions(self):
        return tuple(mod.getActualPosition() for mod in self.modules)

_inst = None

###########################################
## Public API
def getInstance():
    global _inst
    if(_inst is None):
        _inst = _DrivetrainControl()
    return _inst