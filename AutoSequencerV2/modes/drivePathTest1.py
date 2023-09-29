
from AutoSequencerV2.commands.drivePathCommand import DrivePathCommand
from AutoSequencerV2.mode import Mode

# A DrivePathTest1 is an autonomous mode which drives 
#   the specific path designed in the deploy/pathplanner/testPath1.path file
class DrivePathTest1(Mode):
    def __init__(self):
        Mode.__init__(self, f"Drive Path Test 1")
        self.pathCmd = DrivePathCommand("testPath1", 1.0)
        
    def getCmdGroup(self):
        # Just return the path command
        return self.pathCmd
    
    def getInitialDrivetrainPose(self):
        # Use the path command to specify the starting pose
        return self.pathCmd.path.getInitialHolonomicPose()