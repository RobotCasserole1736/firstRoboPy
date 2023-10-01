import wpilib
from dashboard import Dashboard
from humanInterface.driverInterface import DriverInterface
import drivetrain.drivetrainControl as dt
from utils.functionGenerator import FunctionGenerator
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.signalLogging import log
import utils.signalLogging as SignalLogging
import utils.calibration as Calibration
import utils.faults as Faults
from utils.rioMonitor import RIOMonitor
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
        
        self.driveTrain = dt.getInstance()
                
        self.dashboard = Dashboard(self.webserver)
        
        self.dInt = DriverInterface()
        
        self.autoSequencer = AS.getInstance()

        self.rioMonitor = RIOMonitor()
        self.addPeriodic(self.rioMonitor.update500ms, 0.5)

    def robotPeriodic(self):
        self.stt.start()
        self.driveTrain.update()
        log("test", self.fgTest.get())
        SignalLogging.update()
        Calibration.update()
        Faults.update()
        self.rioMonitor.update20ms()
        self.stt.end()
        
    #########################################################
    ## Autonomous-Specific init and update
    def autonomousInit(self):
        # Start up the autonomous sequencer
        self.autoSequencer.initiaize()
        
        # Use the autonomous rouines starting pose to init the pose estimator
        self.driveTrain.poseEst.setKnownPose(self.autoSequencer.getStartingPose())
        
    def autonomousPeriodic(self):
        self.autoSequencer.update()

    def autonomousExit(self):
        self.autoSequencer.end()

    #########################################################
    ## Teleop-Specific init and update
    def teleopInit(self):
        pass
        
    def teleopPeriodic(self):
        self.dInt.update()
        self.driveTrain.setCmdFieldRelative(
            self.dInt.getFwdRevCmd(),
            self.dInt.getStrafeCmd(),
            self.dInt.getRotateCmd())
    
    
    #########################################################
    ## Disabled-Specific init and update
    def disabledPeriodic(self):
        AS.getInstance().updateMode()
        

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
        dt.destroyInstance()
        
        
if __name__ == '__main__':

    # Uncomment these lines to enable debugging the RIO remotely
    import debugpy
    debugpy.listen(('0.0.0.0', 5678))
    #debugpy.wait_for_client()

    wpilib.run(MyRobot)