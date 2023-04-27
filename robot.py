import wpilib
from  utils.signalLogging import log, publish

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        print("It's Init Time")
    
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        log("test", 42)
    
    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        log("test", 23)
        
    def robotPeriodic(self):
        publish()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)