import wpilib

from wpimath.units import metersToFeet
from wpimath.trajectory import Trajectory
from wpimath.geometry import Pose2d
from utils.signalLogging import log
from pathplannerlib.trajectory import PathPlannerTrajectory


class DrivetrainPoseTelemetry():
    """
    Helper class to wrapper sending all drivetrain Pose related information 
    to dashboards
    """
    
    def __init__(self):
        
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("DT Pose 2D", self.field)
        self.curTraj = Trajectory()
        self.desPose = Pose2d()

    def setDesiredPose(self, desPose):
        self.desPose = desPose
        
    def update(self, estPose):
        self.field.getRobotObject().setPose(estPose)
        self.field.getObject("desPose").setPose(self.desPose)
        self.field.getObject("desTraj").setTrajectory(self.curTraj)

        log("DT Pose Est X", metersToFeet(estPose.X()), "ft")
        log("DT Pose Est Y", metersToFeet(estPose.Y()), "ft")
        log("DT Pose Est T", estPose.rotation().degrees(), "deg")
        log("DT Pose Des X", metersToFeet(self.desPose.X()), "ft")
        log("DT Pose Des Y", metersToFeet(self.desPose.Y()), "ft")
        log("DT Pose Des T", self.desPose.rotation().degrees(), "deg")

    def setTrajectory(self, trajIn:PathPlannerTrajectory):
        """Display a specific trajectory on the robot Field2d

        Args:
            trajIn (PathPlannerTrajectory): The trajectory to display
        """
        # Transform pathplanner state into useful trajectory for telemetry
        if trajIn is not None:
            stateList = []
            stateList.append(trajIn.getInitialState())
            for idx in range(1, 10):
                stateList.append(trajIn.sample(trajIn.getTotalTimeSeconds() * (idx/float(10))))
            stateList.append(trajIn.getEndState())

            stateList = [self._pathplannerToWPIState(x) for x in stateList]
            self.curTraj = Trajectory(stateList)
        else:
            self.curTraj = Trajectory()

    # Convert from PathPlanner's state to WPILib's state (for telemetry)
    def _pathplannerToWPIState(self, inVal):
        return Trajectory.State(
            acceleration=inVal.accelerationMpsSq,
            pose=inVal.getTargetHolonomicPose(),
            t=inVal.timeSeconds,
            velocity=inVal.velocityMps
            )
