
from Autonomous.commands.drivePathCommand import DrivePathCommand
from AutoSequencerV2.mode import Mode
from wpimath.geometry import Rotation2d, Pose2d

# A DrivePathTest1 is an autonomous mode which drives 
#   the specific path designed in the deploy/pathplanner/testPath1.path file
class DrivePathTest1(Mode):
    def __init__(self):
        Mode.__init__(self, f"Drive Path Test 1")
        self.pathCmd = DrivePathCommand("TestPath1", 0.75)
        
    def getCmdGroup(self):
        # Just return the path command
        return self.pathCmd
    
    def getInitialDrivetrainPose(self):
        # The first path command can be used to store the starting position
        #  under the assumption the drive team puts it on the field in that spot.
        # However, we must manually specify the expected orientation (since this is
        #  not inside of pathplanner's model of the world)
        startingTrans = self.pathCmd.path.getStartingDifferentialPose().translation()
        startingRotation = Rotation2d.fromDegrees(45.0)
        return Pose2d(startingTrans, startingRotation)