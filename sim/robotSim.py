
# Class which implements a simulation of all robot hardware
from sim.drivetrainSim import DrivetrainSim


class RobotSim():
    
    def __init__(self):
        self.drivetrain = DrivetrainSim()
        
    def update(self):
        self.drivetrain.update()
        
    def reset(self):
        pass # TODO