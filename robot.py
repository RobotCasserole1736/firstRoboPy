import os
import wpilib
from dashboard import Dashboard
from humanInterface.driverInterface import DriverInterface
import drivetrain.drivetrainControl as dt
from utils.segmentTimeTracker import SegmentTimeTracker
import utils.signalLogging as SignalLogging
import utils.calibration as Calibration
import utils.faults as Faults
from utils.crashLogger import CrashLogger
from utils.rioMonitor import RIOMonitor
from webserver.webserver import Webserver
import AutoSequencerV2.autoSequencer as AS
import reportGen


class MyRobot(wpilib.TimedRobot):

    #########################################################
    ## Common init/update for all modes
    def robotInit(self): 
        # Since we're defining a bunch of new things here, tell pylint 
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init

        self.driveTrain = dt.getInstance()


        self.crashLogger = CrashLogger()
        
        wpilib.LiveWindow.disableAllTelemetry()

        self.webserver = Webserver()
                
        self.stt = SegmentTimeTracker()
        
                
        self.dashboard = Dashboard(self.webserver)
        
        self.dInt = DriverInterface()
        
        self.autoSequencer = AS.getInstance()

        self.rioMonitor = RIOMonitor()    
        
        reportGen.generate(self)


    def robotPeriodic(self):
        self.stt.start()
        self.crashLogger.update()
        
        if(self.dInt.getGyroResetCmd()):
            self.driveTrain.resetGyro()
        
        self.driveTrain.update()
        SignalLogging.update()
        Calibration.update()
        Faults.update()
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
            self.dInt.getVxCmd(),
            self.dInt.getVyCmd(),
            self.dInt.getVtCmd())
    
    
    #########################################################
    ## Disabled-Specific init and update
    def disabledPeriodic(self):
        AS.getInstance().updateMode()
        self.driveTrain.trajCtrl.updateCals()

    #########################################################
    ## Test-Specific init and update
    def testInit(self):
        # Induce a crash
        oopsie = (5/0.0) # pylint: disable=unused-variable

    #########################################################
    ## Cleanup
    def endCompetition(self):
        # Our code has a number of things which create "global state",
        # that is to say variables and objects which are not children
        # of the main robot class (including python global variables)
        # We hook the endCompetition method to clean these things up
        # when our code exits.
        # Note this is primarily for unit test support: Usually,
        # our code exits in one of two "abnormal" ways:
        # 1) On Robot: we unplug the RIO
        # 2) In Simulation: The process ends
        self.rioMonitor.stopThreads()
        Faults.destroyInstance()
        dt.destroyInstance()
        super().endCompetition()


        
        
if __name__ == '__main__':

    enableDebug = os.path.isfile("/home/lvuser/py/enableDebug")
    if(enableDebug):
        print("Starting Debug Support....")
        import debugpy 
        debugpy.listen(('0.0.0.0', 5678))
        debugpy.wait_for_client()

    wpilib.run(MyRobot)
