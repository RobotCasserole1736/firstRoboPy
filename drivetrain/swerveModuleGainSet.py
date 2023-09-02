from utils.calibration import Calibration


class SwerveModuleGainSet():
    def __init__(self):
        self.wheel_kP = Calibration("Drivetrain Module Wheel kP", 0.02) 
        self.wheel_kI = Calibration("Drivetrain Module Wheel kI", 0.0)
        self.wheel_kD = Calibration("Drivetrain Module Wheel kD", 0.0)
        self.wheel_kA = Calibration("Drivetrain Module Wheel kA", 0.00,  "volts/radPerSecPerSec")
        self.wheel_kV = Calibration("Drivetrain Module Wheel kV", 0.017, "volts/radPerSec")
        self.wheel_kS = Calibration("Drivetrain Module Wheel kS", 0.12,  "volts")
        self.azmth_kP = Calibration("Drivetrain Module Azmth kP", 0.008)
        self.azmth_kI = Calibration("Drivetrain Module Azmth kI", 0.0)
        self.azmth_kD = Calibration("Drivetrain Module Azmth kD", 0.00001)

    def hasChanged(self):
        return (self.wheel_kP.isChanged() or
                self.wheel_kI.isChanged() or
                self.wheel_kD.isChanged() or
                self.wheel_kA.isChanged() or
                self.wheel_kV.isChanged() or
                self.wheel_kS.isChanged() or
                self.azmth_kP.isChanged() or
                self.azmth_kI.isChanged() or
                self.azmth_kD.isChanged() )