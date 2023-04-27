import wpilib
import utils.signalLogging as sl

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        print("It's Init Time")
    
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        sl.log("test", 42)
    
    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        sl.log("test", 23)
        
    def robotPeriodic(self):
        sl.publish()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)