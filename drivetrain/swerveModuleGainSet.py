from utils.calibration import Calibration


class SwerveModuleGainSet():
    def __init__(self):
        self.wheelP = Calibration("Drivetrain Module Wheel kP", 0.02) 
        self.wheelI = Calibration("Drivetrain Module Wheel kI", 0.0)
        self.wheelD = Calibration("Drivetrain Module Wheel kD", 0.0)
        self.wheelA = Calibration("Drivetrain Module Wheel kA", 0.00,  "volts/radPerSecPerSec")
        self.wheelV = Calibration("Drivetrain Module Wheel kV", 0.017, "volts/radPerSec")
        self.wheelS = Calibration("Drivetrain Module Wheel kS", 0.12,  "volts")
        self.azmthP = Calibration("Drivetrain Module Azmth kP", 0.008)
        self.azmthI = Calibration("Drivetrain Module Azmth kI", 0.0)
        self.azmthD = Calibration("Drivetrain Module Azmth kD", 0.00001)

    def hasChanged(self):
        return (self.wheelP.isChanged() or
                self.wheelI.isChanged() or
                self.wheelD.isChanged() or
                self.wheelA.isChanged() or
                self.wheelV.isChanged() or
                self.wheelS.isChanged() or
                self.azmthP.isChanged() or
                self.azmthI.isChanged() or
                self.azmthD.isChanged() )