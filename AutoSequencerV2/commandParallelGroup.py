

from AutoSequencerV2.commandGroup import CommandGroup

class CommandParallelGroup(CommandGroup):
    def __init__(self, cmdList):
        CommandGroup.__init__(self, cmdList)
        self.cmdFinishedDict = {}

        
    def initialize(self):
        super().initialize()
        
        # Set up the dictionary of commands to "finished" booleans
        self.cmdFinishedDict.clear()
        for cmd in self.cmdList:
            self.cmdFinishedDict[cmd] = False
        
    def execute(self):
        for cmd in self.cmdList:
            if(not self.cmdFinishedDict[cmd]):
                # Run each unfinished command in this group, checking for finish as we go.
                cmd.execute()
                if(cmd.isDone()):
                    #Naturally end the command when it is done.
                    cmd.end(False)
                    self.cmdFinishedDict[cmd] = True
        
    def isDone(self):
        # We're done when every command has finished
        return all(self.cmdFinishedDict.values())
    
    def alongWith(self, other):
        # Special case - when composing two command parallel groups, collapse to a single group
        if(isinstance(other, CommandParallelGroup)):
            mergedCmdList = []
            mergedCmdList.extend(self.cmdList)
            mergedCmdList.extend(other.cmdList)
            return CommandParallelGroup(mergedCmdList)
        else:
            return super().alongWith(other)
    
