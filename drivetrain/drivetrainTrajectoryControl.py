from wpimath.trajectory import Trajectory
from wpimath.geometry import Rotation2d

class SwerveTrajectoryCmd():
    desTrajState = Trajectory.State()
    desAngle = Rotation2d()
    desAngVel = Rotation2d()
