# AutoSequencerV2

Casserole has developed an in-house autonomous coordination infrastrcuture.

Starting in 2023 it got a major overhaul, incorporting a more flexible event/command grouping scheme, and methods to _compose_ things together.

It is intentionally modeled after WPILib's command-based paradigms, but without requriing subsystem architecture. Think of it as both a stepping stone to a full command-based paradigm, without committing to restructuring other code.

The autosequencer is a singleton- there is only ever one sequencer. One sequencer may have multiple mode lists. The selection from each mode list should be concatenated together with an `andThen()` composition.

## Usage - Code

### Main Robot Integration

First, import the webserver class.

```py
from AutoSequencerV2.autoSequencer import as_getInstance
```

Then, call the auto sequencer methods from the three Autonomous methods:

```py
def autonomousInit(self):
    as_getInstance().initiaize()
    
def autonomousPeriodic(self):
    as_getInstance().update()

def autonomousExit(self):
    as_getInstance().end()
```

These methods must always be called in the order of initialize -> update -> end

To allow users to select the mode(s), add an approprate widget.

```py
self.webserver.addDashboardWidget(
    AutoChooser(50, 10, as_getInstance().getDelayModeNTTableName(), 
                as_getInstance().getDelayModeList()))

self.webserver.addDashboardWidget(
    AutoChooser(75, 10, as_getInstance().getMainModeNTTableName(), 
                as_getInstance().getMainModeList()))
```

[More information about adding widgets is found here.](dashboardWidgets.py)

The call to `get*NTTableName()` returns a string, indicating what NetworkTables topic should be used for selecting an autonomous mode.

The call to `get*ModeList()` returns a list of strings, indicating what human-readable name the dashboard should display for modes.

### Creating new Autonomous Modes

First, make a new file, named after the mode you want to have.

Import the generic mode class.

```py
from AutoSequencerV2.mode import Mode
```

Create a new class for your new mode, which extends the base `Mode` class.

```py
class MyNewMode(Mode):

    def getCmdGroup(self):
        # TODO - return a command group that should be run when this mode is selected
        #return WaitCommand(4.0).andThen(WaitCommand(3.0)).andThen(WaitCommand(5.0))
    
    def getInitialDrivetrainPose(self):
        # TODO - Return the Pose2d() of where the robot starts for this mode
        # Ex: return Pose2d(0,0,0)
    
    def getName(self):
        # TODO - Return a custom name for this mode
        # ex: return "leeeroooyy jeeeennnkkinnnsssss"
```

Add the new mode into AutoSequencerV2's `mainModeList` in the constructor

```py
self.mainModeList = ModeList("Main")
self.mainModeList.addMode(DoNothingMode())
self.mainModeList.addMode(MyNewMode())
# TODO - add more autonomous modes here
```