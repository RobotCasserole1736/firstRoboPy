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
    """
    Top-level control class for controlling a swerve drivetrain
    """
    def __init__(self):
        self.modules = []
        self.modules.append(SwerveModuleControl("FL", 0, 1, 0, FL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("FR", 2, 3, 1, FR_ENCODER_MOUNT_OFFSET_RAD, True))
        self.modules.append(SwerveModuleControl("BL", 4, 5, 2, BL_ENCODER_MOUNT_OFFSET_RAD, False))
        self.modules.append(SwerveModuleControl("BR", 6, 7, 3, BR_ENCODER_MOUNT_OFFSET_RAD, True))
        
        self.desChSpd = ChassisSpeeds()
        self.curDesPose = Pose2d()

        self.gains = SwerveModuleGainSet()

        self._updateAllCals()

        self.poseEst = DrivetrainPoseEstimator(self.getModulePositions())
        
        self.trajCtrl = DrivetrainTrajectoryControl()



    def setCmdFieldRelative(self, velX, velY, velT):
        """Send commands to the robot for motion relative to the field

        Args:
            velX (float): Desired speed in the field's X direction, in meters per second
            velY (float): Desired speed in the field's Y axis, in th meters per second
            velT (float): Desired rotational speed in the field's reference frame, in radians per second
        """
        self.desChSpd = ChassisSpeeds.fromFieldRelativeSpeeds(velX, 
                                                              velY, 
                                                              velT, 
                                                              self.poseEst.getCurEstPose().rotation())
        self.poseEst.setDesiredPose(self.poseEst.getCurEstPose()) 

    def setCmdRobotRelative(self, velX, velY, velT):
        """Send commands to the robot for motion relative to its own reference frame

        Args:
            velX (float): Desired speed in the robot's X direction, in meters per second
            velY (float): Desired speed in the robot's Y axis, in th meters per second
            velT (float): Desired rotational speed in the robot's reference frame, in radians per second
        """
        self.desChSpd = ChassisSpeeds(velX, velY, velT)
        self.poseEst.setDesiredPose(self.poseEst.getCurEstPose())
        
    def setCmdTrajectory(self, cmd):
        """Send commands to the robot for motion as a part of following a trajectory

        Args:
            cmd (PathPlannerState): PathPlanner trajectory sample for the current time
        """
        self.desChSpd = self.trajCtrl.update(cmd, self.poseEst.getCurEstPose())
        self.poseEst.setDesiredPose(Pose2d(cmd.pose.translation(), cmd.holonomicRotation))


    def update(self):
        """
        Main periodic update, should be called every 20ms
        """
        
        # Given the current desired chassis speeds, convert to module states
        desModStates = kinematics.toSwerveModuleStates(self.desChSpd)
        
        # Scale back commands if one corner of the robot is going too fast
        kinematics.desaturateWheelSpeeds(desModStates, MAX_FWD_REV_SPEED_MPS)

        # Send commands to modules and update
        for idx, module in enumerate(self.modules):
            module.setDesiredState(desModStates[idx])
            module.update()
            
        # Update the estimate of our pose
        self.poseEst.update(self.getModulePositions())
        
        # Update calibration values if they've changed
        if(self.gains.hasChanged()):
            self._updateAllCals()
            
                
    def _updateAllCals(self):
        # Helper function - udpates calibration on request
        for module in self.modules:
            module.setClosedLoopGains(self.gains)


    def getModulePositions(self):
        """
        Returns:
            Tuple of the actual module positions (as read from sensors)
        """
        return tuple(mod.getActualPosition() for mod in self.modules)


# The actual drivetrain instance
_inst = None

# Necessary singleton cleanup when the robot logic is restarted.
def destroyInstance():
    global _inst
    _inst = None

###########################################
## Public API
def getInstance():
    """Singleton Infrastructure

    Returns:
        the instance of the drivetrain singleton
    """
    global _inst
    if(_inst is None):
        _inst = _DrivetrainControl()
    return _inst