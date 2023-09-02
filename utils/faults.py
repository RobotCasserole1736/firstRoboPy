import math
import wpilib

FIX_ME_LED_PIN = 8
HEARTBEAT_LED_PIN = 9

class _FaultWrangler():
    def __init__(self):
        self.faultList = []
        self.activeFaultCount = 0
        self.loopCounter = 0
        self.statusUpdateLoops = 40 # Only update the status every 40 loops
        self.curDisplayedFaultIdx = 0
        
        self.fixMeLED = wpilib.DigitalOutput(FIX_ME_LED_PIN)
        self.fixMeLED.setPWMRate(500.0)
        self.fixMeLED.enablePWM(1.0) # Initially should be just "ON" until the first call to update
        
        self.heartbeatLED = wpilib.DigitalOutput(HEARTBEAT_LED_PIN)
        self.heartbeatLED.setPWMRate(500.0)
        self.heartbeatLED.enablePWM(1.0) # Initially should be just "ON" until the first call to update
            
    def update(self):
        self.loopCounter += 1
        if(self.loopCounter == self.statusUpdateLoops):
            # Every N loops, Update status String
            activeFaults = [x for x in self.faultList if x.isActive]
            self.activeFaultCount = len(activeFaults)
            self.loopCounter = 0 # reset counter

            if(self.activeFaultCount > 0):
                self.curDisplayedFaultIdx = (self.curDisplayedFaultIdx + 1) % self.activeFaultCount
                curFaultString = activeFaults[self.curDisplayedFaultIdx].message
            else:
                curFaultString = ""

            wpilib.SmartDashboard.putBoolean("faultActive", self.activeFaultCount > 0)
            wpilib.SmartDashboard.putString("faultDescription", curFaultString)


            
        # Update faults LED
        if(self.activeFaultCount > 0):
            self.fixMeLED.updateDutyCycle(self._blinkPattern(1.3))
        else:
            self.fixMeLED.updateDutyCycle(0.0)
            
        # Update heartbeat LED
        self.heartbeatLED.updateDutyCycle(self._blinkPattern(0.75))
        
    # Returns a time-varying blink intensity to drive the LED
    # at a given frequency
    def _blinkPattern(self, freq):
        return abs(math.sin(2 * math.pi * wpilib.Timer.getFPGATimestamp() * freq / 2.0))
    
    def register(self, fault):
        self.faultList.append(fault)
        

_inst = None
def getInstance():
    global _inst
    if(_inst is None):
        _inst = _FaultWrangler()
    return _inst

def destroyInstance():
    global _inst
    _inst = None

   
###########################################
# Public API
###########################################

# Create a new Fault whenever you have a condition for which you can
# annunciate a fault    
class Fault():
    def __init__(self, message):
        self.message = message
        getInstance().register(self)
        self.isActive = False
        
    def set(self, isActive):
        self.isActive = isActive
        
    def setFaulted(self):
        self.isActive = True
        
    def setNoFault(self):
        self.isActive = False
        
# Call this in the main robot loop to keep led's blinking
def update():
    getInstance().update()
