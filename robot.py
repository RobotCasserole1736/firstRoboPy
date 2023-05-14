import wpilib
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.text import Text
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
        
        self.webserver.addDashboardWidget(CircularGauge(15, 15, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(LineGauge(15, 50, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(Text(30, 75, "/SmartDashboard/test"))

    
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
        echokernel.kernelPeriodic()
        publishSignals()
        updateCalibrations()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)