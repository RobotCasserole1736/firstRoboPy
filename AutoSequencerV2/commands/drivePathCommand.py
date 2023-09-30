

import wpilib
from pathplannerlib import PathPlanner

from AutoSequencerV2.command import Command
from drivetrain.drivetrainPhysical import MAX_DT_LINEAR_SPEED
from drivetrain.drivetrainPhysical import MAX_TRANSLATE_ACCEL_MPS2
import drivetrain.drivetrainControl as dt


class DrivePathCommand(Command):
    
    def __init__(self, pathFile, speedScalar):
    
        self.name = pathFile
        self.path = PathPlanner.loadPath(pathFile, 
                                         MAX_DT_LINEAR_SPEED * speedScalar,
                                         MAX_TRANSLATE_ACCEL_MPS2 * speedScalar)  
        self.done = False
        self.startTime = -1 # we'll populate these for real later, just declare they'll exist
        self.duration = self.path.getTotalTime()

    def initialize(self):
        self.startTime = wpilib.Timer.getFPGATimestamp()

    def execute(self):
        curTime = wpilib.Timer.getFPGATimestamp() - self.startTime
        curState = self.path.sample(curTime)

        dt.getInstance().setCmdTrajectory(curState)        

        self.done = curTime >= (self.duration)
        
        if(self.done):
            dt.getInstance().setCmdRobotRelative(0,0,0)

    def isDone(self):
        return self.done
    
    def getName(self):
        return f"Drive Trajectory {self.name}"
