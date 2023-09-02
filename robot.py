import wpilib
from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.camera import Camera, getRIOStreamURL
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
from humanInterface.driverInterface import DriverInterface
from drivetrain.drivetrainControl import DrivetrainControl
from sim.robotSim import RobotSim
from utils.functionGenerator import FunctionGenerator
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.signalLogging import log
import utils.signalLogging as SignalLogging
import utils.calibration as Calibration
import utils.faults as Faults
from webserver.webserver import Webserver
import AutoSequencerV2.autoSequencer as AS

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
        
        self.driveTrain = DrivetrainControl()
        
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
            AutoChooser(50, 10, AS.getInstance().getDelayModeNTTableName(), 
                        AS.getInstance().getDelayModeList()))
        
        self.di = DriverInterface()

    def robotPeriodic(self):
        self.stt.start()
        self.driveTrain.update()
        log("test", self.fgTest.get())
        SignalLogging.update()
        Calibration.update()
        Faults.update()
        self.stt.end()
        
    #########################################################
    ## Autonomous-Specific init and update
    def autonomousInit(self):
        AS.getInstance().initiaize()
        
    def autonomousPeriodic(self):
        AS.getInstance().update()

    def autonomousExit(self):
        AS.getInstance().end()

    #########################################################
    ## Teleop-Specific init and update
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        self.di.update()
        self.driveTrain.setCmdRobotRelative(
            self.di.getFwdRevCmd(),
            self.di.getStrafeCmd(),
            self.di.getRotateCmd())
    
    
    #########################################################
    ## Disabled-Specific init and update
    def disabledPeriodic(self):
        AS.getInstance().updateMode()
        
    #########################################################
    ## Robot Simulation Support
    def _simulationInit(self):
        # pylint: disable=attribute-defined-outside-init
        self.botSim = RobotSim()
    
    def _simulationPeriodic(self):
        self.botSim.update()
        
    #########################################################
    ## Unit Test Support
    def __del__(self):
        # Students! Look away! Do as I say, not as I do!
        #
        #
        # ...
        #
        #
        # Ok since you asked:
        # The FaultWrangler singleton instantiates two WPILIB Hal objeccts 
        # to control the blinky LED's. This is fine on the robot, because the 
        # whole python process is killed and restarted whenever robot code restarts.
        # However, in unit simulations, only this _class_ is destroyed and recreated,
        # which leakes any singleton's state from one test to another. Again, this is
        # _sorta_ ok, because the singletons by definition have to handle abitrary
        # call sequences and data inputs. While it makes the test case order matter,
        # it's not the end of the world. Except for Faults, where we can't re-use the 
        # HAL resource from the previous instantiation. Hence this very not-singleton-pattern
        # call to cleanly destroy our FaultWrangler instance when the robot class is destroyed.
        Faults.destroyInstance()
        
        
if __name__ == '__main__':
    wpilib.run(MyRobot)