import math
from wpimath.controller import PIDController
from wpimath.kinematics import ChassisSpeeds
from utils.calibration import Calibration
from utils.signalLogging import log

class DrivetrainTrajectoryControl():
    """
    Closed-loop controller suite to get the robot from where it is to where it isn't
    https://www.youtube.com/watch?v=bZe5J8SVCYQ
    Used to emulate driver commands while following a trajectory.
    
    This is often called a "Holonomic Drive Controller" or "HDC"
    """
    def __init__(self):
        self.curVx = 0
        self.curVy = 0
        self.curVtheta = 0
        
        self.transP = Calibration("Drivetrain HDC Translation kP", 0) 
        self.transI = Calibration("Drivetrain HDC Translation kI", 0.0)
        self.transD = Calibration("Drivetrain HDC Translation kD", 0.0)
        self.rotP = Calibration("Drivetrain HDC Rotation kP", 0.0) 
        self.rotI = Calibration("Drivetrain HDC Rotation kI", 0.0)
        self.rotD = Calibration("Drivetrain HDC Rotation kD", 0.0)

        # Closed-loop control for the X position
        self.xCtrl = PIDController(
            self.transP.get(),
            self.transI.get(),
            self.transD.get(),
        )
        
        # Closed-loop control for the Y position
        self.yCtrl = PIDController(
            self.transP.get(),
            self.transI.get(),
            self.transD.get(),
        )
        
        # Closed-loop control for rotation (Theta)
        self.tCtrl = PIDController(
            self.rotP.get(),
            self.rotI.get(),
            self.rotD.get(),
        )
        # Make sure the controller knows that -170 and 170 are just 20 degrees apart
        self.tCtrl.enableContinuousInput(-math.pi, math.pi)
    
    def update(self, trajCmd,  curEstPose):
        """Main periodic update, call this whenever you need new commands

        Args:
            trajCmd (PathPlannerState): Current trajectory state
            curEstPose (Pose2d): Current best-estimate of where the robot is at on the field

        Returns:
            ChassisSpeeds: the Field-relative set of vx, vy, and vt commands for 
            the robot to follow that will get it to the desired pose
        """
        
        # Feed-Forward - calculate how fast we should be going at this point in the trajectory
        xFF = trajCmd.velocity * trajCmd.pose.rotation().cos()
        yFF = trajCmd.velocity * trajCmd.pose.rotation().sin()
        tFF = trajCmd.holonomicAngularVelocity
        
        # Feed-Back - Apply additional correction if we're not quite yet at the spot on the field we
        #             want to be at.
        xFB = self.xCtrl.calculate(curEstPose.X(), trajCmd.pose.X())
        yFB = self.yCtrl.calculate(curEstPose.Y(), trajCmd.pose.Y())
        tFB = self.tCtrl.calculate(curEstPose.rotation().radians(), trajCmd.holonomicRotation.radians())
        
        log("Drivetrain HDC xFF", xFF, "mps")
        log("Drivetrain HDC yFF", yFF, "mps")
        log("Drivetrain HDC tFF", tFF, "radpersec")
        
        log("Drivetrain HDC xFB", xFB, "mps")
        log("Drivetrain HDC yFB", yFB, "mps")
        log("Drivetrain HDC tFB", tFB, "radpersec")
    
        return ChassisSpeeds.fromFieldRelativeSpeeds(xFF + xFB, yFF + yFB, tFF + tFB, curEstPose.rotation())