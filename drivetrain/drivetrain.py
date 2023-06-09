

# Class which implements control logic for a 4-module swerve drive
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.signalLogging import log
from wrappers.wrapperedSparkMax import WrapperedSparkMax


class DriveTrain:
    def __init__(self):
        self.testMotor = WrapperedSparkMax(1, "test")
        
    def update(self):
        log(getAzmthDesTopicName("FL"), 0)
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
        
    def setCmdRobotRelative(self, fwdRevMetersPerSec, strafeMetersPerSec, rotateRadiansPerSec):
        pass
    
    def setCmdFieldRelative(self, fwdRevMetersPerSec, strafeMetersPerSec, rotateRadiansPerSec):
        pass   
    
    def setCmdPathplan(self, pathState):
        pass   