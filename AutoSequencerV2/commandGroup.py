from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable
from enum import Enum


# TODO make a new enum-ish class to define the style of group (Parallel, Race, Sequential)

# TODO - pull all the guts of the specific groups into here, and switch based on group type. Also, implement the composition methods here for groups composed with groups for all combos of group types

# class syntax
class GroupType(Enum):
    SEQUENTIAL = 1
    PARALLEL = 2
    RACE = 3


class CommandGroup(Runnable, Composer):
    def __init__(self, cmdList, groupType):
        self.groupType = groupType
        self.cmdList = cmdList
        self.curCmdIdx = 0
        self.cmdFinishedDict = {}
        self.finishedFirstIdx = None # Set to the index of the command which finished first, or None if all are running
        
    def execute(self):
        if(self.groupType == GroupType.RACE):
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
                        
        elif(self.groupType == GroupType.PARALLEL):
            for cmd in self.cmdList:
                if(not self.cmdFinishedDict[cmd]):
                    # Run each unfinished command in this group, checking for finish as we go.
                    cmd.execute()
                    if(cmd.isDone()):
                        #Naturally end the command when it is done.
                        cmd.end(False)
                        self.cmdFinishedDict[cmd] = True
                        
        elif(self.groupType == GroupType.SEQUENTIAL)
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
        else:
            raise(RuntimeError("Unsupported Command Group Type!"))
            
    # Default group init - just init each command
    def initialize(self):
        for cmd in self.cmdList:
            cmd.initialize()
            
    # Default group end - end everything with same interrupted status
    def end(self, interrupted):
        for cmd in self.cmdList:
            cmd.end(interrupted)
            

    
            