class AutoSequencer():
    
    def __init__(self):
        self.delayOptions = [
            0.0,3.0,6.0,9.0
        ]
        self.modeList = []
        self.curCmdSequence = None
        
    def addMode(self, newMode):
        self.modeList.append(newMode)
        
    # Call this periodically while disabled to keep the dashboard updated
    # and, when things change, re-init modes
    def updateMode(self):
        # TODO read from NT from dashboard
        
        # TODO udpate current modes
        
        # TODO if any mode has changed re-init the current command sequence
        pass
    
    # Call this once during autonmous init to init the current command sequence
    def initSequencer(self):
        # TODO set self.curCmdSequence based on current mode(s)
        self.curCmdSequence.initalize()
    
    def update(self):
        self.curCmdSequence.execute()

    def stopSequencer(self):
        if(not self.curCmdSequence.isDone()):
            self.curCmdSequence.end(True)
