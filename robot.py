import wpilib
from utils.functionGenerator import FunctionGenerator
from  utils.signalLogging import log, publishSignals
from utils.calibration import updateCalibrations


class MyRobot(wpilib.TimedRobot):

    def robotInit(self): 
        # Since we're defining a bunch of new things here, tell pylint 
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init
        print("It's Init Time")
        self.fgTest = FunctionGenerator("test")  
    
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        log("test", self.fgTest.get())
    
    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        log("test", 23)
        
    def robotPeriodic(self):
        publishSignals()
        updateCalibrations()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)