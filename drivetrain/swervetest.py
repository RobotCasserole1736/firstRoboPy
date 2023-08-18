import wpilib 
import wpilib.simulation
import rev
# Class which implements control logic for a 4-module swerve drive
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.signalLogging import log

class swerveDriveTest:
    def _init__(self):
       
        self.Motor1 = rev.CANSparkMax(1, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor2 = rev.CANSparkMax(2, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor3 = rev.CANSparkMax(3, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor4 = rev.CANSparkMax(4, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor5 = rev.CANSparkMax(5, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor6 = rev.CANSparkMax(6, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor7 = rev.CANSparkMax(7, rev.CANSparkMax.MotorType.kBrushless)
        self.Motor8 = rev.CANSparkMax(8, rev.CANSparkMax.MotorType.kBrushless)
        print("swerve init complete")


        # Declairing PID Controller so we can use PID features
        self.pidController = self.Motor1.getPIDController()

        # setting PID Coefficents and Controller Output Range
        self.kP = 0.1
        self.kI = 1e-4
        self.kD = 0
        self.kIz = 0
        self.kFF = 0
        self.kMinOutput = -1
        self.kMaxOutput = 1

        # Motor max RPM
        self.maxRPM = 5700


        #setting PID constants
        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)
        self.pidController.setIZone(self.kIz)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(self.kMinOutput, self.kMaxOutput)

        # Push PID Coefficients to SmartDashboard
        wpilib.SmartDashboard.putNumber("P Gain", self.kP)
        wpilib.SmartDashboard.putNumber("I Gain", self.kI)
        wpilib.SmartDashboard.putNumber("D Gain", self.kD)
        wpilib.SmartDashboard.putNumber("I Zone", self.kIz)
        wpilib.SmartDashboard.putNumber("Feed Forward", self.kFF)
        wpilib.SmartDashboard.putNumber("Min Output", self.kMinOutput)
        wpilib.SmartDashboard.putNumber("Max Output", self.kMaxOutput)


    def update(self): 


        #getting data from the smart dashboard, there may be a better way to do this that wouldn't make us use smartdashboard but I dont know 
        p = wpilib.SmartDashboard.getNumber("P Gain", 0)
        i = wpilib.SmartDashboard.getNumber("I Gain", 0)
        d = wpilib.SmartDashboard.getNumber("D Gain", 0)
        iz = wpilib.SmartDashboard.getNumber("I Zone", 0)
        ff = wpilib.SmartDashboard.getNumber("Feed Forward", 0)
        min_out = wpilib.SmartDashboard.getNumber("Min Output", 0)
        max_out = wpilib.SmartDashboard.getNumber("Max Output", 0)

        driverController = wpilib.XboxController(0)

        # Defining controller /\

        controllerLX = driverController.getLeftX 
        controllerLY = driverController.getLeftY
        controllerRX = driverController.getRightX
        controllerRY = driverController.getRightY

        # defining stick inputs /\

        motorEncoder = self.Motor1.getEncoder()

        # defining encoder values /\


        


        