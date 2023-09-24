import wpilib


class DrivetrainPoseTelemetry():
    
    def __init__(self):
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("DT Pose 2D", self.field)
        
    def update(self, estPose, desPose):
        self.field.getObject("estPose").setPose(estPose)
        self.field.getObject("desPose").setPose(desPose)