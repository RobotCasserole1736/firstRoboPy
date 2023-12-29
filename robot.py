import os
import wpilib
from Autonomous.modes.drivePathTest1 import DrivePathTest1
from dashboard import Dashboard
from humanInterface.driverInterface import DriverInterface
from drivetrain.drivetrainControl import DrivetrainControl
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.signalLogging import SignalWrangler
from utils.calibration import CalibrationWrangler
from utils.faults import FaultWrangler
from utils.crashLogger import CrashLogger
from utils.rioMonitor import RIOMonitor
from utils.singleton import destroyAllSingletonInstances
from webserver.webserver import Webserver
from AutoSequencerV2.autoSequencer import AutoSequencer

class MyRobot(wpilib.TimedRobot):

    #########################################################
    ## Common init/update for all modes
    def robotInit(self): 
        # Since we're defining a bunch of new things here, tell pylint 
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init

        self.crashLogger = CrashLogger()
        wpilib.LiveWindow.disableAllTelemetry()
        
        self.stt = SegmentTimeTracker()
        # self.stt.doOptionalPerhapsMarks = True # Uncomment this line to turn on optional stt perhapsMark methods
        # self.stt.longLoopThresh = 0.020 # Uncomment this line adjust the stt logging time threshold in seconds
        #                                                                        1         2         3
        #                                                               12345678901234567890123456789012345
        self.markStartCrashName          = self.stt.makePaddedMarkName("start-crashLogger")
        self.markCrashName               = self.stt.makePaddedMarkName("crashLogger")
        self.markResetGyroName           = self.stt.makePaddedMarkName("driveTrain.resetGyro")
        self.markDriveTrainName          = self.stt.makePaddedMarkName("driveTrain.update")
        self.markSignalWranglerName      = self.stt.makePaddedMarkName("SignalWrangler().publishPeriodic")
        self.markCalibrationWranglerName = self.stt.makePaddedMarkName("CalibrationWrangler().update")
        self.markFautWranglerName        = self.stt.makePaddedMarkName("FaultWrangler().update()")

        self.webserver = Webserver()


        self.driveTrain = DrivetrainControl()
                
        self.dInt = DriverInterface()
        
        self.autoSequencer = AutoSequencer()
        self.autoSequencer.addMode(DrivePathTest1())

        self.dashboard = Dashboard()

        self.rioMonitor = RIOMonitor()
        
        
        # Uncomment this and simulate to update the code 
        # dependencies graph
        # from codeStructureReportGen import reportGen
        # reportGen.generate(self)


    def robotPeriodic(self):
        self.stt.start()

        self.stt.perhapsMark(self.markStartCrashName)
        self.crashLogger.update()
        self.stt.perhapsMark(self.markCrashName)

        if(self.dInt.getGyroResetCmd()):
            self.driveTrain.resetGyro()
        self.stt.perhapsMark(self.markResetGyroName)

        self.driveTrain.update()
        self.stt.perhapsMark(self.markDriveTrainName)

        SignalWrangler().publishPeriodic()
        self.stt.perhapsMark(self.markSignalWranglerName)

        CalibrationWrangler().update()
        self.stt.perhapsMark(self.markCalibrationWranglerName)

        FaultWrangler().update()
        self.stt.perhapsMark(self.markFautWranglerName)

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
        self.autoSequencer.updateMode()
        self.driveTrain.trajCtrl.updateCals()

    #########################################################
    ## Test-Specific init and update
    def testInit(self):
        # Induce a crash
        oopsie = (5/0.0) # pylint: disable=unused-variable

    #########################################################
    ## Cleanup
    def endCompetition(self):
        self.rioMonitor.stopThreads()
        destroyAllSingletonInstances()
        super().endCompetition()


if __name__ == '__main__':

    enableDebug = os.path.isfile("/home/lvuser/py/enableDebug")
    if(enableDebug):
        print("Starting Debug Support....")
        import debugpy 
        debugpy.listen(('0.0.0.0', 5678))
        debugpy.wait_for_client()

    wpilib.run(MyRobot)
