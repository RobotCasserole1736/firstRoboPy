import wpilib 
import wpilib.simulation

# Class which implements control logic for a 4-module swerve drive
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.signalLogging import log

#(wpilib.timedRobot):
class DrivetrainControl():
    def __init__(self):
        self.rightMotor1 = wpilib.Spark(4)
        self.rightMotor2 = wpilib.Spark(5)
        self.rightMotor3 = wpilib.Spark(6)
        self.leftMotor1 = wpilib.Spark(7)
        self.leftMotor2 = wpilib.Spark(8)
        self.leftMotor3 = wpilib.Spark(9)
        print("drive init complete")
        
        
    def update(self):
        log(getAzmthDesTopicName("FL"), 0)## Do we need all of these logs?
        log(getAzmthActTopicName("FL"), 5)
        log(getSpeedDesTopicName("FL"), 10)
        log(getSpeedActTopicName("FL"), 15)
        log(getAzmthDesTopicName("FR"), 20)
        log(getAzmthActTopicName("FR"), 25)
        log(getSpeedDesTopicName("FR"), 30)
        log(getSpeedActTopicName("FR"), 35)
        log(getAzmthDesTopicName("BL"), 40)
        log(getAzmthActTopicName("BL"), 45)
        log(getSpeedDesTopicName("BL"), 50)
        log(getSpeedActTopicName("BL"), 55)
        log(getAzmthDesTopicName("BR"), 60)
        log(getAzmthActTopicName("BR"), 65)
        log(getSpeedDesTopicName("BR"), 70)
        log(getSpeedActTopicName("BR"), 75)

        drivercontroller = wpilib.XboxController(0)

        rightFwdRevCmd = drivercontroller.getRightY()
        leftTurnRevCmd = drivercontroller.getLeftX()

        rightMotorControl = rightFwdRevCmd + leftTurnRevCmd 
        leftMotorControl = rightFwdRevCmd - leftTurnRevCmd 
        
        if leftMotorControl > 1:
            leftMotorControl = 1
        elif leftMotorControl < -1:
            leftMotorControl = -1
        
        if rightMotorControl > 1: 
            rightMotorControl = 1
        elif rightMotorControl < -1:
            rightMotorControl = -1

        rightMotorControl = rightMotorControl * -1 

        
        self.leftMotor1.set(leftMotorControl)
        self.leftMotor2.set(leftMotorControl)
        self.leftMotor3.set(leftMotorControl)
        self.rightMotor1.set(rightMotorControl)
        self.rightMotor2.set(rightMotorControl)
        self.rightMotor3.set(rightMotorControl)
        """
        elif  rightFwdRevCmd > 0.25 or rightFwdRevCmd < -0.25:

            self.leftMotor1.set(0)
            self.leftMotor2.set(0)
            self.leftMotor3.set(0)
            self.rightMotor1.set(0)
            self.rightMotor2.set(0)
            self.rightMotor3.set(0)
            
            

            self.rightMotor1.set(rightFwdRevCmd)
            self.rightMotor2.set(rightFwdRevCmd)
            self.rightMotor3.set(rightFwdRevCmd)

        else:

            self.rightMotor1.set(0.0)
            self.rightMotor2.set(0.0)
            self.rightMotor3.set(0.0)
            self.leftMotor1.set(0.0)
            self.leftMotor2.set(0.0)
            self.leftMotor3.set(0.0)
            """
