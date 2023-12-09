
from Autonomous.commands.drivePathCommand import DrivePathCommand
from AutoSequencerV2.mode import Mode

# A DrivePathCircle is an autonomous mode which in a simple circle with some rotation
class DrivePathCircleNoRotate(Mode):
    def __init__(self):
        Mode.__init__(self, f"Drive Path No Spin")
        self.pathCmd = DrivePathCommand("nospin")
        
    def getCmdGroup(self):
        # Just return the path command
        return self.pathCmd
    
    def getInitialDrivetrainPose(self):
        # Use the path command to specify the starting pose
        return self.pathCmd.path.getInitialPose()