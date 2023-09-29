import math
from wpimath.controller import PIDController
from wpimath.kinematics import ChassisSpeeds
from utils.calibration import Calibration
from utils.signalLogging import log

class DrivetrainTrajectoryControl():
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
        self.tCtrl.enableContinuousInput(-math.pi, math.pi)
    
    def update(self, trajCmd,  curEstPose):
        xFF = trajCmd.velocity * trajCmd.pose.rotation().cos()
        yFF = trajCmd.velocity * trajCmd.pose.rotation().sin()
        tFF = trajCmd.holonomicAngularVelocity
        
        
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