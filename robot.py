import wpilib
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
from drivetrain.drivetrain import Drivetrain
from sim.robotSim import RobotSim
from utils.functionGenerator import FunctionGenerator
from  utils.signalLogging import log, publishSignals
from utils.calibration import updateCalibrations
from webserver.webserver import Webserver


class MyRobot(wpilib.TimedRobot):

    #########################################################
    ## Common init/update for all modes
    def robotInit(self): 
        # Since we're defining a bunch of new things here, tell pylint 
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init
        self.fgTest = FunctionGenerator("test")
        self.webserver = Webserver()
        log("test", -1, "rpm")
        
        self.dt = Drivetrain()
        
        self.webserver.addDashboardWidget(CircularGauge(15, 15, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(LineGauge(15, 50, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(Text(30, 75, "/SmartDashboard/test"))
        self.webserver.addDashboardWidget(SwerveState(75, 15))

    def robotPeriodic(self):
        self.dt.update()
        log("test", self.fgTest.get())
        publishSignals()
        updateCalibrations()
        
    #########################################################
    ## Autonomous-Specific init and update
    def autonomousInit(self):
        pass
        
    def autonomousPeriodic(self):
        pass
        
    
    #########################################################
    ## Teleop-Specific init and update
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        pass


        
    #########################################################
    ## Robot Simulation Support
    def _simulationInit(self):
        # pylint: disable=attribute-defined-outside-init
        self.botSim = RobotSim()
    
    def _simulationPeriodic(self):
        self.botSim.update()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)