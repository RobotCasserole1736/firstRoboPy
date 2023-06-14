



from AutoSequencerV2.commandGroup import CommandGroup


class CommandSequentialGroup(CommandGroup):
    def __init__(self, cmdList):
        CommandGroup.__init__(self, cmdList)
        self.curCmdIdx = 0
        
    def initialize(self):
        super().initialize()
        self.curCmdIdx = 0
        if(self.curCmdIdx < len(self.cmdList)):
            # Init the first command
            curCmd = self.cmdList[self.curCmdIdx]
            curCmd.initialize()
        
    def execute(self):
        if(self.curCmdIdx < len(self.cmdList)):
            # If we've got a valid command, execute it
            curCmd = self.cmdList[self.curCmdIdx]
            curCmd.execute()
            
            if(curCmd.isDone()):
                # Time to move on to the next command
                # First, Naturally end the current command
                curCmd.end(False)
                # Move onto the next command
                self.curCmdIdx += 1
                # Init it if it exists
                if(self.curCmdIdx < len(self.cmdList)):
                    curCmd = self.cmdList[self.curCmdIdx]
                    curCmd.initalize()
                    # That's it, next loop we'll execute it.
                
    def end(self, interrupted):
        # Only need to end the current command
        curCmd = self.cmdList[self.curCmdIdx]
        curCmd.end(interrupted)

    def isDone(self):
        # We're done when we hit the end of the list
        return self.curCmdIdx >= len(self.cmdList)
    
    def andThen(self, other):
        # Special case - when composing two command sequential groups, collapse to a single group
        if(isinstance(other, CommandSequentialGroup)):
            mergedCmdList = []
            mergedCmdList.extend(self.cmdList)
            mergedCmdList.extend(other.cmdList)
            return CommandSequentialGroup(mergedCmdList)
        else:
            return super().andThen(other)
    