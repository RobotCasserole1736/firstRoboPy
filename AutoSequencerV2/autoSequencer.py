from AutoSequencerV2.commandGroup import CommandGroup
from AutoSequencerV2.modeList import ModeList
from AutoSequencerV2.modes.doNothingMode import DoNothingMode
from AutoSequencerV2.modes.waitMode import WaitMode


class _AutoSequencer():
    def __init__(self):
        
        self.delayModeList = ModeList("Delay")
        self.delayModeList.addMode(WaitMode(0.0))
        self.delayModeList.addMode(WaitMode(3.0))
        self.delayModeList.addMode(WaitMode(6.0))
        self.delayModeList.addMode(WaitMode(9.0))
        
        self.mainModeList = ModeList("Main")
        self.mainModeList.addMode(DoNothingMode())
        # TODO - add more autonomous modes here
        
        self.topLevelCmdGroup = CommandGroup()
        
        self.updateMode(force=True) # Ensure we load the auto sequener at least once.
        
        
    # Call this periodically while disabled to keep the dashboard updated
    # and, when things change, re-init modes
    def updateMode(self, force=False):
        mainChanged = self.mainModeList.updateMode()
        delayChanged = self.delayModeList.updateMode()
        if(mainChanged or delayChanged or force):
            mainMode = self.mainModeList.getCurMode()
            delayMode = self.delayModeList.getCurMode()
            self.topLevelCmdGroup = delayMode.getCmdGroup().andThen(mainMode.getCmdGroup())
            print(f"[Auto] New Modes Selected: {delayMode.getName()}, {mainMode.getName()}")

    
    # Call this once during autonmous init to init the current command sequence
    def initiaize(self):  
        print("[Auto] Starting Sequencer")
        self.topLevelCmdGroup.initialize()
    
    def update(self):
        self.topLevelCmdGroup.execute()

    def end(self):
        self.topLevelCmdGroup.end(True)
        print("[Auto] Sequencer Stopped")
        
    def getMainModeList(self):
        return self.mainModeList.getNames()
    
    def getMainModeNTTableName(self):
        return self.mainModeList.getModeTopicBase()

    def getDelayModeList(self):
        return self.delayModeList.getNames()
    
    def getDelayModeNTTableName(self):
        return self.delayModeList.getModeTopicBase()

# Singleton-ish instance for main thread only.
_autoSequencerInst = _AutoSequencer()

###########################################
## Public API
def getInstance():
    return _autoSequencerInst