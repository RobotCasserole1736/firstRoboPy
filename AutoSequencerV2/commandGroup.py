from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable
from enum import Enum


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

    ##################################################
    ## Race group operation

    def _initRace(self):
        self.finishedFirstIdx = None

        # Init all the cmds
        for cmd in self.cmdList:
            cmd.initialize()

    def _executeRace(self):
        if(self.finishedFirstIdx != None):
            if(not self.isDone()):
                for idx, cmd in enumerate(self.cmdList):
                    # Run each command in this group, checking for finish as we go.
                    cmd.execute()
                    if(cmd.isDone()):
                        # If we're finished, stop updating
                        self.finishedFirstIdx = idx
                        break

    def _endRace(self, interrupted):
        # Finish each child command
        for idx, cmd in enumerate(self.cmdList):
            isInterrupted = False if idx == self.finishedFirstIdx else True or interrupted
            cmd.end(self, isInterrupted)

    def _isDoneRace(self):
        #We're done when one command has finished
        return (self.finishedFirstIdx != None)


    ##################################################
    ## Parallel group operation
    def _initParallel(self):
        # Set up the dictionary of commands to "finished" booleans
        self.cmdFinishedDict.clear()
        for cmd in self.cmdList:
            self.cmdFinishedDict[cmd] = False
        
        for cmd in self.cmdList:
            cmd.initialize()

    def _executeParallel(self):
        for cmd in self.cmdList:
            if(not self.cmdFinishedDict[cmd]):
                # Run each unfinished command in this group, checking for finish as we go.
                cmd.execute()
                if(cmd.isDone()):
                    #Naturally end the command when it is done.
                    cmd.end(False)
                    self.cmdFinishedDict[cmd] = True

    def _endParallel(self, interrupted):
        for cmd in self.cmdList:
            if(not self.cmdFinishedDict[cmd]):
                # End all unfinished commands
                cmd.end(interrupted)

    def _isDoneParallel(self):
        # We're done when every command has finished
        return all(self.cmdFinishedDict.values())
    
    ##################################################
    ## Sequential group operation

    def _initSequential(self):
        self.curCmdIdx = 0
        if(self.curCmdIdx < len(self.cmdList)):
            # Init the first command
            curCmd = self.cmdList[self.curCmdIdx]
            curCmd.initialize()

    def _executeSequential(self):
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
                    curCmd.initialize()
                    # That's it, next loop we'll execute it.

    def _endSequential(self, interrupted):
        # Only need to end the current command
        curCmd = self.cmdList[self.curCmdIdx]
        curCmd.end(interrupted)

    def _isDoneSequential(self):
        # We're done when we hit the end of the list
        return self.curCmdIdx >= len(self.cmdList)

    ##################################################
    ## common method switchyard

    def execute(self):
        if(self.groupType == GroupType.RACE):
            self._executeRace()
        elif(self.groupType == GroupType.PARALLEL):
            self._executeParallel()
        elif(self.groupType == GroupType.SEQUENTIAL):
            self._executeSequential()
        else:
            raise(RuntimeError("Unsupported Command Group Type!"))
            
    # Default group init - just init each command
    def initialize(self):
        if(self.groupType == GroupType.RACE):
            self._initRace()
        elif(self.groupType == GroupType.PARALLEL):
            self._initParallel()
        elif(self.groupType == GroupType.SEQUENTIAL):
            self._initSequential()
        else:
            raise(RuntimeError("Unsupported Command Group Type!"))
            
    # Default group end - end everything with same interrupted status
    def end(self, interrupted):
        if(self.groupType == GroupType.RACE):
            self._endRace(interrupted)
        elif(self.groupType == GroupType.PARALLEL):
            self._endParallel(interrupted)
        elif(self.groupType == GroupType.SEQUENTIAL):
            self._endSequential(interrupted)
        else:
            raise(RuntimeError("Unsupported Command Group Type!"))
        
    def isDone(self):
        if(self.groupType == GroupType.RACE):
            self._isDoneRace()
        elif(self.groupType == GroupType.PARALLEL):
            self._isDoneParallel()
        elif(self.groupType == GroupType.SEQUENTIAL):
            self._isDoneSequential()
        else:
            raise(RuntimeError("Unsupported Command Group Type!"))

    ##################################################
    ## composition handlers

    def andThen(self, other):
        return self._composeWith(other, GroupType.SEQUENTIAL)
    
    def raceWith(self, other):
        return self._composeWith(other, GroupType.RACE)

    def alongWith(self, other):
        return self._composeWith(other, GroupType.PARALLEL)

    def _composeWith(self, other, outputGroupType):
        if(isinstance(other, CommandGroup) and other.groupType == outputGroupType and self.groupType == outputGroupType):
            cmds = []
            cmds.extend(self.cmdList)
            cmds.extend(other.cmdList)
        else:
            cmds = [self, other]
        return CommandGroup(cmds, outputGroupType)
            

    
            