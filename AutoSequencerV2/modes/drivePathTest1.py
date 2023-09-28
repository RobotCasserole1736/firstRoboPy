
from AutoSequencerV2.commands.drivePathCommand import DrivePathCommand
from AutoSequencerV2.mode import Mode

# A DoNothingMode is an autonomous mode where the robot just sits doing nothing indefinitely
class DrivePathTest1(Mode):
    def __init__(self):
        # Build a reasonable name out of the specified duration
        Mode.__init__(self, f"Drive Path Test 1")
        self.pathCmd = DrivePathCommand("testPath1", 1.0)
        
    def getCmdGroup(self):
        # A wait mode should have only one command, jsut wait the specified duration
        return self.pathCmd
    
    def getInitialDrivetrainPose(self):
        return self.pathCmd.path.getInitialPose()