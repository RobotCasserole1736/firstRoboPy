import wpilib
from wpimath.units import metersToFeet
from wpimath.trajectory import Trajectory
from utils.signalLogging import log



class DrivetrainPoseTelemetry():
    
    def __init__(self):
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("DT Pose 2D", self.field)
        
    def update(self, estPose, desPose, trajectory=Trajectory()):
        self.field.getRobotObject().setPose(estPose)
        self.field.getObject("desPose").setPose(desPose)
        self.field.getRobotObject().setTrajectory(trajectory)
        log("DT Pose Est X", metersToFeet(estPose.X()), "ft")
        log("DT Pose Est Y", metersToFeet(estPose.Y()), "ft")
        log("DT Pose Est T", estPose.rotation().degrees(), "deg")
        log("DT Pose Des X", metersToFeet(desPose.X()), "ft")
        log("DT Pose Des Y", metersToFeet(desPose.Y()), "ft")
        log("DT Pose Des T", desPose.rotation().degrees(), "deg")