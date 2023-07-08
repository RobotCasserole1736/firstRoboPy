from rev import CANSparkMax, CANSparkMaxLowLevel
from utils.signalLogging import log
from utils.units import rev2Rad, RPM2RadPerSec

class WrapperedSparkMax():
    def __init__(self, canID, name):
        self.ctrl = CANSparkMax(canID, CANSparkMaxLowLevel.MotorType.kBrushless)
        self.pidCtrl = self.ctrl.getPIDController()
        self.encoder = self.ctrl.getEncoder()
        self.name = name
        
    def setInverted(self, isInverted):
        self.ctrl.setInverted(isInverted)
    
    def setPID(self, kP, kI, kD):
        self.pidCtrl.setP(kP)
        self.pidCtrl.setI(kI)
        self.pidCtrl.setD(kD)
    
    def setVoltage(self, outputVoltageVolts):
        log(self.name + "_cmdVoltage", outputVoltageVolts, "V")
        self.ctrl.setVoltage(outputVoltageVolts)
    
    def getCurrent(self):
        current = self.ctrl.getOutputCurrent()
        log(self.name + "_outputCurrent", current, "A")
        return current
    
    def getMotorPositionRad(self):
        pos =  rev2Rad(self.encoder.getPosition())
        log(self.name + "_motorPos", pos, "rad")
        return pos
    
    def getMotorVelocityRadPerSec(self):
        pos = RPM2RadPerSec(self.encoder.getVelocity())
        log(self.name + "_motorVel", pos, "radPerSec")
        return pos