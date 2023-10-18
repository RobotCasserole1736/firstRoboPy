

class _DrivetrainControl():
    """
    Top-level control class for controlling a swerve drivetrain
    """
    def __init__(self):
        pass




    def setCmdFieldRelative(self, velX, velY, velT):
        pass

    def setCmdRobotRelative(self, velX, velY, velT):
        pass
        
    def setCmdTrajectory(self, cmd):
        pass


    def update(self):
        # TODO put code here!
        pass
            
                


    def getModulePositions(self):
        """
        Returns:
            Tuple of the actual module positions (as read from sensors)
        """
        pass
    
    def resetGyro(self):
        pass


# The actual drivetrain instance
_inst = None

# Necessary singleton cleanup when the robot logic is restarted.
def destroyInstance():
    global _inst
    _inst = None

###########################################
## Public API
def getInstance():
    """Singleton Infrastructure

    Returns:
        the instance of the drivetrain singleton
    """
    global _inst
    if(_inst is None):
        _inst = _DrivetrainControl()
    return _inst