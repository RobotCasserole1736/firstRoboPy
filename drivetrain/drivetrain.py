

# Class which implements control logic for a 4-module swerve drive
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.signalLogging import log
import wpilib 
import wpilib.simulation
#(wpilib.timedRobot):
class DriveTrain:
    def __init__(self):
        self.r1 = wpilib.Spark(4)
        self.r2 = wpilib.Spark(5)
        self.r3 = wpilib.Spark(6)
        self.l1 = wpilib.Spark(7)
        self.l2 = wpilib.Spark(8)
        self.l3 = wpilib.Spark(9)
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

        
        self.l1.set(leftMotorControl)
        self.l2.set(leftMotorControl)
        self.l3.set(leftMotorControl)
        self.r1.set(rightMotorControl)
        self.r2.set(rightMotorControl)
        self.r3.set(rightMotorControl)
        '''
        elif  rightFwdRevCmd > 0.25 or rightFwdRevCmd < -0.25:

            self.l1.set(0)
            self.l2.set(0)
            self.l3.set(0)
            self.r1.set(0)
            self.r2.set(0)
            self.r3.set(0)
            
            

            self.r1.set(rightFwdRevCmd)
            self.r2.set(rightFwdRevCmd)
            self.r3.set(rightFwdRevCmd)

        else:

            self.r1.set(0.0)
            self.r2.set(0.0)
            self.r3.set(0.0)
            self.l1.set(0.0)
            self.l2.set(0.0)
            self.l3.set(0.0)
            '''

        


