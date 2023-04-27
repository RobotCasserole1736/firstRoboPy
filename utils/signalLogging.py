import os
import wpilib
import ntcore as nt
import wpiutil._wpiutil.log as wpilog

# Wrangler for coordinating the set of all signals
class _SignalWrangler:

    # Starts up logging to file, along with network tables infrastructure
    # Picks approprate logging directory based on our current target
    def __init__(self):
        # Default to publishing things under Shuffleboard, which makes things more avaialble
        self.table = nt.NetworkTableInstance.getDefault().getTable("Shuffleboard")
        self.publishedSigDict = {}
        self.sampleList = []

        if wpilib.RobotBase.isSimulation():
            logDir = "./simulationLogs"
        else:
            logDir = "/U/logs"

        if not os.path.isdir(logDir):
            os.makedirs(logDir)

        wpilib.DataLogManager.start(dir=logDir)
        wpilib.DriverStation.startDataLog(wpilib.DataLogManager.getLog())
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

                # Set up log file publishing
                sigLog = wpilog.DoubleLogEntry(log=self.log, name=name)

                # Remember handles for both
                self.publishedSigDict[name] = (sigPub, sigLog)

            # Publish value to NT
            self.publishedSigDict[name][0].set(value, time)
            # Put value to log file
            self.publishedSigDict[name][1].append(value, time)

        # Reset sample list back to empty for next loop
        self.sampleList = []

    # Tack on a new floating point number sample
    def addSampleForThisLoop(self, name, value):
        self.sampleList.append((name, value))


# Singleton-ish instance for main thread only.
_mainInst = _SignalWrangler()

###########################################
# Public API
###########################################

# Log a new named value
def log(name, value):
    _mainInst.addSampleForThisLoop(name, value)

# Call once per robot periodic loop
def publish():
    _mainInst.publishPeriodic()
