from wpimath.controller import PIDController
from utils.calibration import Calibration
from wpimath.kinematics import ChassisSpeeds
from utils.signalLogging import log

import math

class DrivetrainTrajectoryControl():
    def __init__(self):
        self.curVx = 0
        self.curVy = 0
        self.curVtheta = 0
        
        self.hdc_trans_kP = Calibration("Drivetrain HDC Translation kP", 0) 
        self.hdc_trans_kI = Calibration("Drivetrain HDC Translation kI", 0.0)
        self.hdc_trans_kD = Calibration("Drivetrain HDC Translation kD", 0.0)
        self.hdc_rot_kP = Calibration("Drivetrain HDC Rotation kP", 0.0) 
        self.hdc_rot_kI = Calibration("Drivetrain HDC Rotation kI", 0.0)
        self.hdc_rot_kD = Calibration("Drivetrain HDC Rotation kD", 0.0)

        self.hdc_x = PIDController(
            self.hdc_trans_kP.get(),
            self.hdc_trans_kI.get(),
            self.hdc_trans_kD.get(),
        )
        
        self.hdc_y = PIDController(
            self.hdc_trans_kP.get(),
            self.hdc_trans_kI.get(),
            self.hdc_trans_kD.get(),
        )
        
        self.hdc_t = PIDController(
            self.hdc_rot_kP.get(),
            self.hdc_rot_kI.get(),
            self.hdc_rot_kD.get(),
        )
        self.hdc_t.enableContinuousInput(-math.pi, math.pi)
    
    def update(self, trajCmd,  curEstPose):
        xFF = trajCmd.velocity * trajCmd.pose.rotation().cos()
        yFF = trajCmd.velocity * trajCmd.pose.rotation().sin()
        tFF = trajCmd.holonomicAngularVelocity
        
        
        xFB = self.hdc_x.calculate(curEstPose.X(), trajCmd.pose.X())
        yFB = self.hdc_y.calculate(curEstPose.Y(), trajCmd.pose.Y())
        tFB = self.hdc_t.calculate(curEstPose.rotation().radians(), trajCmd.holonomicRotation.radians())
        
        log("Drivetrain HDC xFF", xFF, "mps")
        log("Drivetrain HDC yFF", yFF, "mps")
        log("Drivetrain HDC tFF", tFF, "radpersec")
        
        log("Drivetrain HDC xFB", xFB, "mps")
        log("Drivetrain HDC yFB", yFB, "mps")
        log("Drivetrain HDC tFB", tFB, "radpersec")
    
        return ChassisSpeeds.fromFieldRelativeSpeeds(xFF + xFB, yFF + yFB, tFF + tFB, curEstPose.rotation())