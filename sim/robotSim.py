
# Class which implements a simulation of all robot hardware
from sim.drivetrainSim import DrivetrainSim


class RobotSim():
    
    def __init__(self):
        self.dt = DrivetrainSim()
        
    def update(self):
        self.dt.update()