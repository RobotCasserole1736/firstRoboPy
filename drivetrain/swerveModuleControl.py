from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.controller import PIDController
from wpimath.kinematics import SwerveModuleState
from wpimath.kinematics import SwerveModulePosition
from wpimath.geometry import Rotation2d

from wrappers.wrapperedSparkMax import WrapperedSparkMax
from wrappers.wrapperedSRXMagEncoder import WrapperedSRXMagEncoder
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.signalLogging import log
from utils.units import rad2Deg
from drivetrain.drivetrainPhysical import dtMotorRotToLinear_m
from drivetrain.drivetrainPhysical import dtLinearToMotorRot_rad
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS

class SwerveModuleControl():
    def __init__(self, moduleName, wheelMotorCanID, azmthMotorCanID, azmthEncoderPortIdx, azmthOffset, invertWheel):
        self.wheelMotor = WrapperedSparkMax(wheelMotorCanID, moduleName+"_wheel", False)
        self.azmthMotor = WrapperedSparkMax(azmthMotorCanID, moduleName+"_azmth", True)
        self.azmthEnc  = WrapperedSRXMagEncoder(azmthEncoderPortIdx, moduleName + "_azmthEnc", azmthOffset, False)

        self.wheelMotor.setInverted(invertWheel)
        self.azmthMotor.setInverted(True)
        
        self.wheelMotorFF = SimpleMotorFeedforwardMeters(0,0,0)

        self.desiredState = SwerveModuleState()
        self.optimizedDesiredState = SwerveModuleState()
        self.actualState = SwerveModuleState()

        self.azmthCtrl = PIDController(0,0,0)
        self.azmthCtrl.enableContinuousInput(-180.0, 180.0)

        self.moduleName = moduleName

    def updateTelemetry(self):
        log(getAzmthDesTopicName(self.moduleName), self.optimizedDesiredState.angle.degrees(), "deg")
        log(getAzmthActTopicName(self.moduleName), rad2Deg(self.azmthEnc.getAngleRad()), "deg")
        log(getSpeedDesTopicName(self.moduleName), self.optimizedDesiredState.speed/MAX_FWD_REV_SPEED_MPS, "frac")
        log(getSpeedActTopicName(self.moduleName), dtMotorRotToLinear_m(self.wheelMotor.getMotorVelocityRadPerSec())/MAX_FWD_REV_SPEED_MPS, "frac")

    def getActualPosition(self):
        wheelPosMeters = dtMotorRotToLinear_m(self.wheelMotor.getMotorPositionRad())
        return SwerveModulePosition(wheelPosMeters, Rotation2d(self.azmthEnc.getAngleRad()))

    def getActualState(self):
        return self.actualState

    def getDesiredState(self):
        return self.desiredState

    def setClosedLoopGains(self, 
                           wheel_kP, 
                           wheel_kI, 
                           wheel_kD, 
                           wheel_kA, 
                           wheel_kV, 
                           wheel_kS, 
                           azmth_kP, 
                           azmth_kI, 
                           azmth_kD):
        self.wheelMotor.setPID(wheel_kP, wheel_kI, wheel_kD)
        self.wheelMotorFF = SimpleMotorFeedforwardMeters(wheel_kS, wheel_kV, wheel_kA)
        self.azmthCtrl.setPID(azmth_kP, azmth_kI, azmth_kD)

    def setDesiredState(self, desState):
        self.desiredState = desState


    def update(self):

        # Read from the azimuth angle sensor (encoder)
        self.azmthEnc.update()

        # Optimize our incoming swerve command to minimize motion
        self.optimizedDesiredState = SwerveModuleState.optimize(self.desiredState, Rotation2d(self.azmthEnc.getAngleRad()))

        # Use a PID controller to calculate the voltage for the azimuth motor
        self.azmthCtrl.setSetpoint(self.optimizedDesiredState.angle.degrees())
        azmthVoltage = self.azmthCtrl.calculate(rad2Deg(self.azmthEnc.getAngleRad()))
        self.azmthMotor.setVoltage(azmthVoltage)

        # Send voltage and speed commands to the wheel motor
        motorDesSpd_radpersec = dtLinearToMotorRot_rad(self.optimizedDesiredState.speed)
        motorVoltageFF = self.wheelMotorFF.calculate(motorDesSpd_radpersec)
        self.wheelMotor.setVelCmd(motorDesSpd_radpersec, motorVoltageFF)

        # Update this module's actual state with measurements from the sensors
        self.actualState.angle = Rotation2d(self.azmthEnc.getAngleRad())
        self.actualState.speed = dtMotorRotToLinear_m(self.wheelMotor.getMotorVelocityRadPerSec)

