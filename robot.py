import wpilib
from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.camera import Camera, getRIOStreamURL
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
from drivetrain.drivetrain import DriveTrain
from sim.robotSim import RobotSim
from utils.functionGenerator import FunctionGenerator
from utils.segmentTimeTracker import SegmentTimeTracker
from  utils.signalLogging import log, publishSignals
from utils.calibration import updateCalibrations
from webserver.webserver import Webserver
from AutoSequencerV2.autoSequencer import *

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
                
        self.stt = SegmentTimeTracker()
        
        self.driveTrain = DriveTrain()
        
        wpilib.CameraServer.launch()
        
        self.webserver.addDashboardWidget(
            CircularGauge(15, 15, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(
            LineGauge(15, 50, "/SmartDashboard/test", -10,10,-5,5))
        self.webserver.addDashboardWidget(
            Text(30, 75, "/SmartDashboard/test"))
        self.webserver.addDashboardWidget(
            SwerveState(85, 15))
        self.webserver.addDashboardWidget(
            Camera(75, 60, getRIOStreamURL(1181)))
        self.webserver.addDashboardWidget(
            AutoChooser(50, 10, autosequener_getInstance().getDelayModeNTTableName(), 
                        autosequener_getInstance().getDelayModeList()))

    def robotPeriodic(self):
        self.stt.start()
        self.driveTrain.update()
        log("test", self.fgTest.get())
        publishSignals()
        updateCalibrations()
        self.stt.end()
        
    #########################################################
    ## Autonomous-Specific init and update
    def autonomousInit(self):
        autosequener_getInstance().initiaize()
        
    def autonomousPeriodic(self):
        autosequener_getInstance().update()

    def autonomousExit(self):
        autosequener_getInstance().end()

        
    
    #########################################################
    ## Teleop-Specific init and update
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        pass
    
    
    #########################################################
    ## Disabled-Specific init and update
    def disabledPeriodic(self):
        autosequener_getInstance().updateMode()
        
    #########################################################
    ## Robot Simulation Support
    def _simulationInit(self):
        # pylint: disable=attribute-defined-outside-init
        self.botSim = RobotSim()
    
    def _simulationPeriodic(self):
        self.botSim.update()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)