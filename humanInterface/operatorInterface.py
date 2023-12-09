from wpilib.interfaces._interfaces import GenericHID
from utils.faults import Fault
from utils.signalLogging import log
from wpilib  import Timer


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


    def update(self):
        """Main update - call this once every 20ms
        """
        
        if(self.ctrl.isConnected()):
            # Only attempt to read from the joystick if it's plugged in
            
            # Convert from joystic sign/axis conventions to robot velocity conventions
            vXJoyRaw = -1.0*self.ctrl.getRawAxis(0)
            vYJoyRaw = -1.0*self.ctrl.getRawAxis(1)
            vTJoyRaw = -1.0*self.ctrl.getRawAxis(2)
            
            outval = int(Timer.getFPGATimestamp()) % 2 == 0
            self.ctrl.setOutput( 1 , outval)
            self.ctrl.setOutput( 2 , not outval)
            # self.ctrl.setRumble(GenericHID.RumbleType.kLeftRumble, 0.25)
            # self.ctrl.setRumble(GenericHID.RumbleType.kRightRumble, 0.75)
            
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
