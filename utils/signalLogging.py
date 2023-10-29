import os
import wpilib
import ntcore as nt
import wpiutil._wpiutil.log as wpilog # pylint: disable=import-error,no-name-in-module

from utils.faults import Fault 


BASE_TABLE = "SmartDashboard"

# Wrangler for coordinating the set of all signals
class _SignalWrangler:

    # Starts up logging to file, along with network tables infrastructure
    # Picks approprate logging directory based on our current target
    def __init__(self):
        # Default to publishing things under Shuffleboard, which makes things more avaialble
        self.table = nt.NetworkTableInstance.getDefault().getTable(BASE_TABLE)
        self.publishedSigDict = {}
        self.sigUnitsDict = {}
        self.sampleList = []
        self.enableDiskLogging = True
        self.driveAvailableFault = Fault("Logging USB Drive Not Available")


        if wpilib.RobotBase.isSimulation():
            self.logDir = "./simulationLogs"
        else:
            self.logDir = "/U/logs"

        try:
            if not os.path.isdir(self.logDir):
                os.makedirs(self.logDir)
        except PermissionError as err:
            print("Logging disabled!")
            print(err)
            self.enableDiskLogging = False
            self.driveAvailableFault.setFaulted()

        if(self.enableDiskLogging):
            wpilib.DataLogManager.start(dir=self.logDir)
            wpilib.DataLogManager.logNetworkTables(False) # We have a lot of things in NT that don't need to be logged
            self.log = wpilib.DataLogManager.getLog()

    # Periodic value update
    # Should be called once per periodic loop
    # Synchronously puts all `log()`'ed numbers to both disc and
    # Will empty all the samples from the sampleList and put them into NT and disk

    def publishPeriodic(self):
        time = nt._now() # pylint: disable=W0212
        for sample in self.sampleList:
            name = sample[0]
            value = sample[1]

            if not name in self.publishedSigDict:
                # New signal found!

                # Set up NT publishing
                sigTopic = self.table.getDoubleTopic(name)
                sigPub = sigTopic.publish(nt.PubSubOptions(
                    sendAll=True, keepDuplicates=True))
                sigPub.setDefault(0)
                
                if name in self.sigUnitsDict:
                    unitsStr = self.sigUnitsDict[name]
                    sigTopic.setProperty("units", str(unitsStr))

                # Set up log file publishing if enabled
                if(self.enableDiskLogging):
                    sigLog = wpilog.DoubleLogEntry(log=self.log, name=name)
                else:
                    sigLog = None

                # Remember handles for both
                self.publishedSigDict[name] = (sigPub, sigLog)

            # Publish value to NT
            self.publishedSigDict[name][0].set(value, time)
            # Put value to log file
            if(self.enableDiskLogging):
                self.publishedSigDict[name][1].append(value, time)

        # Reset sample list back to empty for next loop
        self.sampleList = []

    # Tack on a new floating point number sample
    def addSampleForThisLoop(self, name, value):
        self.sampleList.append((name, value))
        
    def getLogDir(self):
        return self.logDir

# Singleton-ish instance for main thread only.
_inst = None
def getInstance():
    global _inst
    if(_inst is None):
        _inst = _SignalWrangler()
    return _inst


###########################################
# Public API
###########################################

# Log a new named value
def log(name, value, units=None):
    getInstance().addSampleForThisLoop(name, value)
    if units is not None :
        getInstance().sigUnitsDict[name] = units

# Call once per robot periodic loop
def update():
    getInstance().publishPeriodic()

def sigNameToNT4TopicName(name):
    return f"/{BASE_TABLE}/{name}"