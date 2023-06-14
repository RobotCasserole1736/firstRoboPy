

from wpimath.geometry import Pose2d
from AutoSequencerV2.command import Command


class Mode():
    def __init__(self):
        pass
    
    def getCmds(self):
        return Command()
    
    def getInitialDrivetrainPose(self):
        return Pose2d(0,0,0)
    
    def getName(self):
        return self.__qualname__