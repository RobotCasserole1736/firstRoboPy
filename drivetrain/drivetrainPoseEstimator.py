from wpimath.geometry import Pose2d, Rotation2d
from wpilib import ADXRS450_Gyro 
from wpimath.estimator import SwerveDrive4PoseEstimator
from drivetrain.drivetrainPhysical import kinematics

class DrivetrainPoseEstimator():
    def __init__(self, initialModuleStates):
        self.curEstPose = Pose2d()
        self.gyro = ADXRS450_Gyro()
        self.poseEst = SwerveDrive4PoseEstimator(
            kinematics,
            self.gyro.getRotation2d(),
            initialModuleStates,
            self.curEstPose
        )
        self.lastModulePositions = initialModuleStates
        self.curRawGyroAngle = Rotation2d()

    def setKnownPose(self, knownPose):
        self.poseEst.resetPosition(self.gyro.getRotation2d(), self.lastModulePositions, knownPose)

    def update(self, curModulePositions):
        self.curRawGyroAngle = self.gyro.getRotation2d()
        self.poseEst.update(self.curRawGyroAngle, curModulePositions)
        self.lastModulePositions = curModulePositions
        self.curEstPose = self.poseEst.getEstimatedPosition()

    def getCurEstPose(self):
        return self.curEstPose

    

