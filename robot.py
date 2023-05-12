import wpilib
from dashboardWidgets.circularGauge import CircularGauge
from utils.functionGenerator import FunctionGenerator
from  utils.signalLogging import log, publishSignals
from utils.calibration import updateCalibrations
from webserver.webserver import Webserver


class MyRobot(wpilib.TimedRobot):

    def robotInit(self): 
        # Since we're defining a bunch of new things here, tell pylint 
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init
        self.fgTest = FunctionGenerator("test")
        self.webserver = Webserver()
        log("test", -1, "rpm")
        
        self.webserver.addDashboardWidget(CircularGauge(10, 10, "/SmartDashboard/test", -10,10,-5,5))

    
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        pass
    
    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        pass
        
    def robotPeriodic(self):
        log("test", self.fgTest.get())
        publishSignals()
        updateCalibrations()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)