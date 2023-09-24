from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.controller import PIDController
from wpimath.kinematics import SwerveModuleState
from wpimath.kinematics import SwerveModulePosition
from wpimath.geometry import Rotation2d
import wpilib

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
        log(getAzmthDesTopicName(self.moduleName), 
            self.optimizedDesiredState.angle.degrees(), "deg")
        log(getAzmthActTopicName(self.moduleName), 
            rad2Deg(self.azmthEnc.getAngleRad()), "deg")
        log(getSpeedDesTopicName(self.moduleName), 
            self.optimizedDesiredState.speed/MAX_FWD_REV_SPEED_MPS, "frac")
        log(getSpeedActTopicName(self.moduleName), 
            dtMotorRotToLinear_m(self.wheelMotor.getMotorVelocityRadPerSec())/MAX_FWD_REV_SPEED_MPS, "frac")

    def getActualPosition(self):
        wheelPosMeters = dtMotorRotToLinear_m(self.wheelMotor.getMotorPositionRad())
        return SwerveModulePosition(wheelPosMeters, Rotation2d(self.azmthEnc.getAngleRad()))

    def getActualState(self):
        return self.actualState

    def getDesiredState(self):
        return self.desiredState

    def setClosedLoopGains(self, gains):
        
        self.wheelMotor.setPID(gains.wheel_kP.get(), 
                               gains.wheel_kI.get(), 
                               gains.wheel_kD.get())
        self.wheelMotorFF = SimpleMotorFeedforwardMeters(gains.wheel_kS.get(), 
                                                         gains.wheel_kV.get(), 
                                                         gains.wheel_kA.get())
        self.azmthCtrl.setPID(gains.azmth_kP.get(), 
                              gains.azmth_kI.get(), 
                              gains.azmth_kD.get())

    def setDesiredState(self, desState):
        self.desiredState = desState


    def update(self):

        # Read from the azimuth angle sensor (encoder)
        self.azmthEnc.update()

        # Optimize our incoming swerve command to minimize motion
        self.optimizedDesiredState = SwerveModuleState.optimize(self.desiredState, Rotation2d(self.azmthEnc.getAngleRad()))

        # Use a PID controller to calculate the voltage for the azimuth motor
        self.azmthCtrl.setSetpoint(self.optimizedDesiredState.angle.degrees()) # type: ignore - I think robotpy has the wrong typehint specified
        azmthVoltage = self.azmthCtrl.calculate(rad2Deg(self.azmthEnc.getAngleRad()))
        self.azmthMotor.setVoltage(azmthVoltage)

        # Send voltage and speed commands to the wheel motor
        motorDesSpd_radpersec = dtLinearToMotorRot_rad(self.optimizedDesiredState.speed)
        motorVoltageFF = self.wheelMotorFF.calculate(motorDesSpd_radpersec)
        self.wheelMotor.setVelCmd(motorDesSpd_radpersec, motorVoltageFF)

        if(wpilib.TimedRobot.isSimulation()):
            # Simulation - assume module is perfect and goes to where we want it to
            self.actualState = self.optimizedDesiredState
        else:
            # Real Robot
            # Update this module's actual state with measurements from the sensors
            self.actualState.angle = Rotation2d(self.azmthEnc.getAngleRad())
            self.actualState.speed = dtMotorRotToLinear_m(self.wheelMotor.getMotorVelocityRadPerSec())

        self.updateTelemetry()

