import wpilib
from pathplannerlib import PathPlannerTrajectory


from wpimath.units import metersToFeet
from wpimath.trajectory import Trajectory
from utils.signalLogging import log
from wpimath.geometry import Pose2d



class _DrivetrainPoseTelemetry():
    
    def __init__(self):
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("DT Pose 2D", self.field)
        self.curTraj = Trajectory()
        
    def update(self, estPose, desPose):
        self.field.getRobotObject().setPose(estPose)
        self.field.getObject("desPose").setPose(desPose)
        self.field.getRobotObject().setTrajectory(self.curTraj)

        log("DT Pose Est X", metersToFeet(estPose.X()), "ft")
        log("DT Pose Est Y", metersToFeet(estPose.Y()), "ft")
        log("DT Pose Est T", estPose.rotation().degrees(), "deg")
        log("DT Pose Des X", metersToFeet(desPose.X()), "ft")
        log("DT Pose Des Y", metersToFeet(desPose.Y()), "ft")
        log("DT Pose Des T", desPose.rotation().degrees(), "deg")

    def setTrajectory(self, trajIn):
        # Transform pathplanner state into useful trajectory for telemetry
        if trajIn is not None:
            stateList = []
            stateList.append(trajIn.getInitialState())
            for idx in range(1, 10):
                stateList.append(trajIn.sample(trajIn.getTotalTime() * (idx/float(10))))
            stateList.append(trajIn.getEndState())

            stateList = [self._pathplannerToWPIState(x) for x in stateList]
            self.curTraj = Trajectory(stateList)
        else:
            self.curTraj = Trajectory()

    # PathPlanner has a built in "to-wpilib" representation, but it doesn't
    # account for holonomic heading. Fix that.
    def _pathplannerToWPIState(self, inVal):
        trans = inVal.pose.translation()
        rot = inVal.holonomicRotation
        pose = Pose2d(trans, rot)
        return Trajectory.State(
            acceleration=inVal.acceleration,
            pose=pose,
            t=inVal.time,
            velocity=inVal.velocity
            )


        

_inst = None

###########################################
## Public API
def getInstance():
    global _inst
    if(_inst is None):
        _inst = _DrivetrainPoseTelemetry()
    return _inst