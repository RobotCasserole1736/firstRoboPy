

from AutoSequencerV2.commandGroup import CommandGroup
from AutoSequencerV2.commandParallelGroup import CommandParallelGroup
from AutoSequencerV2.commandSequentialGroup import CommandSequentialGroup


class CommandRaceGroup(CommandGroup):
    def __init__(self, cmdList):
        CommandGroup.__init__(self, cmdList)
        self.finishedFirstIdx = None # Set to the index of the command which finished first, or None if all are running
        
    def execute(self):
        if(not self.isDone()):
            for idx, cmd in enumerate(self.cmdList):
                # Run each command in this group, checking for finish as we go.
                cmd.execute()
                if(cmd.isDone()):
                    # If we're finished, stop updating
                    self.finishedFirstIdx = idx
                    break
                
            if(self.finishedFirstIdx != None):
                # if we have "naturally" finished the group, end each child command
                for idx, cmd in enumerate(self.cmdList):
                    isInterrupted = False if idx == self.finishedFirstIdx else True
                    cmd.end(self, isInterrupted)
        
    def isDone(self):
        # We're finished when the one command finishes
        return self.finishedFirstIdx != None
    
    def raceWith(self, other):
        # Special case - when composing two command race groups, collapse to a single group
        if(isinstance(other, CommandRaceGroup)):
            mergedCmdList = []
            mergedCmdList.extend(self.cmdList)
            mergedCmdList.extend(other.cmdList)
            return CommandRaceGroup(mergedCmdList)
        else:
            return super().raceWith(other)
        
    def andThen(self, other):
        cmds = [self, other]
        return CommandSequentialGroup(cmds)

    def alongWith(self, other):
        cmds = [self,other]
        return CommandParallelGroup(cmds)