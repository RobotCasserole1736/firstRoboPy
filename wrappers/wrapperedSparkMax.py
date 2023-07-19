from rev import CANSparkMax, CANSparkMaxLowLevel, SparkMaxPIDController, REVLibError
from utils.signalLogging import log
from utils.units import rev2Rad, RPM2RadPerSec
from utils.faults import Fault

## Wrappered Spark Max
# Wrappers REV's libraries to add the following functionality for spark max controllers:
# Grouped PID controller, Encoder, and motor controller objects
# Physical unit conversions into SI units (radians)
# Retry logic for initial configuration
# Fault handling for not crashing code if the motor controller is disconnected
# Fault annunication logic to trigger warnings if a motor couldn't be configured
class WrapperedSparkMax():
    def __init__(self, canID, name, idleMode = CANSparkMax.IdleMode.kCoast):
        self.ctrl = CANSparkMax(canID, CANSparkMaxLowLevel.MotorType.kBrushless)
        self.pidCtrl = self.ctrl.getPIDController()
        self.encoder = self.ctrl.getEncoder()
        self.name = name
        self.connected = False
        self.disconFault = Fault(f"Spark Max {name} ID {canID} disconnected")
        
        # Perform motor configuration, tracking errors and retrying until we have success
        retryCounter = 0
        success = False
        while(not success and retryCounter < 10):
            retryCounter += 1
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
            else:
                success = True
                
        if(not success):
            self.connected = False
            
        self.disconFault.set(not self.connected)
        
    def setInverted(self, isInverted):
        if(self.connected):
            self.ctrl.setInverted(isInverted)
    
    def setPID(self, kP, kI, kD):
        if(self.connected):
            self.pidCtrl.setP(kP)
            self.pidCtrl.setI(kI)
            self.pidCtrl.setD(kD)
        
    def setVelCmd(self, velCmd, arbFF=0):
        if(self.connected):
            self.pidCtrl.setReference(velCmd, CANSparkMax.ControlType.kVelocity, 
                                    0, arbFF, SparkMaxPIDController.ArbFFUnits.kVoltage)

    def setVoltage(self, outputVoltageVolts):
        log(self.name + "_cmdVoltage", outputVoltageVolts, "V")
        if(self.connected):
            self.ctrl.setVoltage(outputVoltageVolts)
    
    def getCurrent(self):
        if(self.connected):
            current = self.ctrl.getOutputCurrent()
        else:
            current = 0
        log(self.name + "_outputCurrent", current, "A")
        return current
    
    def getMotorPositionRad(self):
        if(self.connected):
            pos =  rev2Rad(self.encoder.getPosition())
        else:
            pos = 0
        log(self.name + "_motorActPos", pos, "rad")
        return pos
    
    def getMotorVelocityRadPerSec(self):
        if(self.connected):
            vel = RPM2RadPerSec(self.encoder.getVelocity())
        else:
            vel = 0
        log(self.name + "_motorActVel", vel, "radPerSec")
        return vel