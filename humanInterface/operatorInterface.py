from wpilib.interfaces._interfaces import GenericHID
from wpimath import applyDeadband
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS, MAX_ROTATE_ACCEL_RAD_PER_SEC_2, MAX_ROTATE_SPEED_RAD_PER_SEC, MAX_STRAFE_SPEED_MPS, MAX_TRANSLATE_ACCEL_MPS2
from utils.faults import Fault
from utils.signalLogging import log
from wpilib  import Timer
from wpimath.filter import SlewRateLimiter


class OperatorInterface():
    """Class to gather input from the driver of the robot 
    """

    def __init__(self):
        ctrlIdx = 1
        self.ctrl = GenericHID(ctrlIdx)
        self.velXCmd = 0
        self.velYCmd = 0
        self.velTCmd = 0
        self.gyroResetCmd = False
        self.connectedFault = Fault(f"Operator HID Controller ({ctrlIdx}) Unplugged")

        self.velXSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velYSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velTSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_ROTATE_ACCEL_RAD_PER_SEC_2)


    def update(self):
        """Main update - call this once every 20ms
        """
        
        if(self.ctrl.isConnected()):
            # Only attempt to read from the joystick if it's plugged in
            
            # Convert from joystic sign/axis conventions to robot velocity conventions
            vXJoyRaw = -1.0*self.ctrl.getRawAxis(0)
            vYJoyRaw = 1.0*self.ctrl.getRawAxis(1)
            vTJoyRaw = 1.0*self.ctrl.getRawAxis(2)

            # Apply deadband to make sure letting go of the joystick actually stops the bot
            vXJoy = applyDeadband(vXJoyRaw,0.1)
            vYJoy = applyDeadband(vYJoyRaw,0.1)
            vTJoy = applyDeadband(vTJoyRaw,0.1)
            
            # Normally robot goes half speed - unlock full speed on 
            # sprint command being active
            sprintMult = 1.0 if(self.ctrl.getRawButton(1)) else 0.5

            #Gyro reset Command
            self.gyroResetCmd = self.ctrl.getRawButton(2)

            # Convert joystick fractions into physical units of velocity
            velXCmdRaw = vXJoy * MAX_FWD_REV_SPEED_MPS * sprintMult
            velYCmdRaw = vYJoy * MAX_STRAFE_SPEED_MPS * sprintMult
            velTCmdRaw = vTJoy * MAX_ROTATE_SPEED_RAD_PER_SEC
            
            # Slew-rate limit the velocity units to not change faster than
            # the robot can physically accomplish
            self.velXCmd = self.velXSlewRateLimiter.calculate(velXCmdRaw)
            self.velYCmd = self.velYSlewRateLimiter.calculate(velYCmdRaw)
            self.velTCmd = self.velTSlewRateLimiter.calculate(velTCmdRaw) 
            
            outval = int(Timer.getFPGATimestamp()) % 2 == 0
            self.ctrl.setOutput( 1 , outval)
            self.ctrl.setOutput( 2 , not outval)
            self.ctrl.setOutput( 3 , self.ctrl.getRawButton(1))
            self.ctrl.setOutput( 4 , self.ctrl.getRawButton(2))

            self.connectedFault.setNoFault()
        else:
            vXJoyRaw = 0
            vYJoyRaw = 0
            vTJoyRaw = 0
            # If the joystick is unplugged, pick safe-state commands and raise a fault
            self.connectedFault.setFaulted()

        log("OI X", vXJoyRaw, "")
        log("OI Y", vYJoyRaw, "")
        log("OI Z", vTJoyRaw, "")
        log("OI connected", self.ctrl.isConnected(), "bool")

    def getVxCmd(self):
        """
        Returns:
            float: Driver's current vX (downfield/upfield, or fwd/rev) command in meters per second
        """
        return self.velXCmd

    def getVyCmd(self):
        """
        Returns:
            float: Driver's current vY (side-to-side or strafe) command in meters per second
        """
        return self.velYCmd
    
    def getVtCmd(self):
        """
        Returns:
            float: Driver's current vT (rotation) command in radians per second
        """
        return self.velTCmd
    
    
    def getGyroResetCmd(self):
        """_summary_
        
        Returns:
            boolean: True if the driver wants to reset the gyro, false otherwise
        """
        return self.gyroResetCmd
    
