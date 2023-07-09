from rev import CANSparkMax, CANSparkMaxLowLevel, SparkMaxPIDController, REVLibError
from utils.signalLogging import log
from utils.units import rev2Rad, RPM2RadPerSec

class WrapperedSparkMax():
    def __init__(self, canID, name, idleMode = CANSparkMax.IdleMode.kCoast):
        self.ctrl = CANSparkMax(canID, CANSparkMaxLowLevel.MotorType.kBrushless)
        self.pidCtrl = self.ctrl.getPIDController()
        self.encoder = self.ctrl.getEncoder()
        self.name = name
        
        # Perform motor configuration, tracking errors and retrying until we have success
        success = False
        while(not success):
            errList = []
            errList.append(self.ctrl.restoreFactoryDefaults())
            errList.append(self.ctrl.setIdleMode(idleMode))
            errList.append(self.ctrl.setSmartCurrentLimit(40))
            # Status 0 = Motor output and Faults
            errList.append(self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus0, 20)) 
            # Status 1 = Motor velocity & electrical data
            errList.append(self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus1, 60))
            # Status 2 = Motor Position
            errList.append(self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus2, 65500))
            # Status 3 = Analog Sensor Input
            errList.append(self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus3, 65500))
            if(any(x is not REVLibError.kOk for x in errList)):
                print(f"Failure configuring Spark Max {name} CAN ID {canID}, retrying...")
        
    def setInverted(self, isInverted):
        self.ctrl.setInverted(isInverted)
    
    def setPID(self, kP, kI, kD):
        self.pidCtrl.setP(kP)
        self.pidCtrl.setI(kI)
        self.pidCtrl.setD(kD)
        
    def setVelCmd(self, velCmd, arbFF=0):
        self.pidCtrl.setReference(velCmd, CANSparkMax.ControlType.kVelocity, 
                                  0, arbFF, SparkMaxPIDController.ArbFFUnits.kVoltage)

    def setVoltage(self, outputVoltageVolts):
        log(self.name + "_cmdVoltage", outputVoltageVolts, "V")
        self.ctrl.setVoltage(outputVoltageVolts)
    
    def getCurrent(self):
        current = self.ctrl.getOutputCurrent()
        log(self.name + "_outputCurrent", current, "A")
        return current
    
    def getMotorPositionRad(self):
        pos =  rev2Rad(self.encoder.getPosition())
        log(self.name + "_motorActPos", pos, "rad")
        return pos
    
    def getMotorVelocityRadPerSec(self):
        pos = RPM2RadPerSec(self.encoder.getVelocity())
        log(self.name + "_motorActVel", pos, "radPerSec")
        return pos