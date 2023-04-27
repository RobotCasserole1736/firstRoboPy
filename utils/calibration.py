
class _CalibrationWrangler():

    # Starts up logging to file, along with network tables infrastructure
    # Picks approprate logging directory based on our current target
    def __init__(self):
        pass


# Singleton-ish instance for main thread only.
_mainInst = _CalibrationWrangler()

###########################################
# Public API
###########################################

class Calibration():
    def __init__(self):
        # TODO register this thing with the wrangler
        pass

    def isChanged(self):
        # TODO
        return False

    def get(self):
        # TODO
        return 0
