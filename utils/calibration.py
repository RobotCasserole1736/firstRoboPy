import wpilib
import ntcore as nt

class _CalibrationWrangler():

    # Starts up logging to file, along with network tables infrastructure
    # Picks approprate logging directory based on our current target
    def __init__(self):
        self.calDict = {}
        
    def register(self, cal):
        self.calDict[cal.name] = cal
        
    def update(self):
        for cal in self.calDict.values():
            cal.update()
        
    


# Singleton-ish instance for main thread only.
_wranglerInst = _CalibrationWrangler()

###########################################
# Public API
###########################################

def updateCalibrations():
    _wranglerInst.update()

class Calibration():
    def __init__(self, name, default=0, units="", minVal=float('-99999999'), maxVal=float('99999999')):
        self.name = name
        self.units = units
        self._default = float(default)
        self._lastUpdateTime = 0
        self.min = minVal
        self.max = maxVal
        self._desValue = self._default
        self._curValue = self._default
        self._changed = False
        
        self.reset()
        
        # Set up nt 
        table = nt.NetworkTableInstance.getDefault().getTable("Calibrations")
        
        self.curValTopic = table.getDoubleTopic(name + "/curValue")
        self.curValuePublisher = self.curValTopic.publish(nt.PubSubOptions(
                                    sendAll=False, keepDuplicates=False))
        self.curValuePublisher.setDefault(self._default)
        
        self.curValTopic.setProperty("units", str(self.units))
        self.curValTopic.setProperty("min_cal", float(self.min))
        self.curValTopic.setProperty("max_cal", float(self.max))
        self.curValTopic.setProperty("default_val", float(self._default))
        self.curValTopic.setProperty("pending", False)
        
        desValueTopic = table.getDoubleTopic(name + "/desValue")
        self.desValueSubscriber = desValueTopic.subscribe(self._default)
        
        _wranglerInst.register(self)
        
    # Resets the value of the calibration back to its default
    def reset(self):
        self._desValue = self._default
        self._curValue = self._default
        self._changed = False

    # Provides a new value to the calibration. This value will be returned on the next
    # call to `get()`. The `isChanged()` flag will return True until `get()` is called.
    def set(self, newVal):
        if self.max >= newVal >= self.min:
            self._changed = True
            self._desValue = newVal
        else:
            wpilib.reportWarning(f"[Calibration] Skipping value update for {self.name}," +
                                 " value {newVal} is out of range [{self.min},{self.max}]")
        
    # Periodic update to read from the desired value on NT, and publish the current value
    def update(self):
        val = self.desValueSubscriber.getAtomic()
        if val.time > self._lastUpdateTime :
            self.set(val.value)
            self._lastUpdateTime = val.time
        self.curValuePublisher.set(self._curValue)
        self.curValTopic.setProperty("pending", self._changed)
        
    # Returns True if the value is different than the last time `get()` was called. False otherwise.
    def isChanged(self):
        return self._changed

    # Gets the current value of the calibration, resetting state internally with
    # the assumption the user's code is consuming the value and doing something useful with it.
    def get(self):
        self._curValue = self._desValue
        self._changed = False
        return self._curValue
