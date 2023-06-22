from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable
from enum import Enum


# Defines the style of execution a group should have. 
class GroupType(Enum):
    SEQUENTIAL = 1
    PARALLEL = 2
    RACE = 3

    """Command Group - implements all types of command groups.
    CMG Note: This feels very not-pythonic. However, because commands need to know about commandGroups to do composition,
    but commandGroups need to know about commands to run them, you tend to get circular imports which python hates.
    I'm not sure there's a better way around this
    """
class CommandGroup(Runnable, Composer):
    def __init__(self, cmdList=[], groupType=GroupType.SEQUENTIAL):
        self.groupType = groupType
        self.cmdList = cmdList
        self._curCmdIdx = 0
        self._cmdFinishedDict = {}
        self._finishedFirstIdx = None # Set to the index of the command which finished first, or None if all are running

    ##################################################
    ## Race group operation

    def _initRace(self):
        self._finishedFirstIdx = None

        # Init all the cmds
        for cmd in self.cmdList:
            print(f"[Auto] Start {cmd.getName()}")
            cmd.initialize()

    def _executeRace(self):
        if(not self.isDone()):
            for idx, cmd in enumerate(self.cmdList):
                # Run each command in this group, checking for finish as we go.
                cmd.execute()
                if(cmd.isDone()):
                    # If we're finished, stop updating
                    print(f"[Auto] {cmd.getName()} finished first")
                    self._finishedFirstIdx = idx
                    break

    def _endRace(self, interrupted):
        # Finish each child command
        for idx, cmd in enumerate(self.cmdList):
            isInterrupted = False if idx == self._finishedFirstIdx else True or interrupted
            print(f"[Auto] Ending {cmd.getName()}")
            cmd.end(isInterrupted)

    def _isDoneRace(self):
        #We're done when one command has finished
        return (self._finishedFirstIdx != None)


    ##################################################
    ## Parallel group operation
    def _initParallel(self):
        # Set up the dictionary of commands to "finished" booleans
        self._cmdFinishedDict.clear()
        for cmd in self.cmdList:
            self._cmdFinishedDict[cmd] = False
        
        for cmd in self.cmdList:
            print(f"[Auto] Start {cmd.getName()}")
            cmd.initialize()

    def _executeParallel(self):
        for cmd in self.cmdList:
            if(not self._cmdFinishedDict[cmd]):
                # Run each unfinished command in this group, checking for finish as we go.
                cmd.execute()
                if(cmd.isDone()):
                    #Naturally end the command when it is done.
                    print(f"[Auto] {cmd.getName()} finished")
                    cmd.end(False)
                    self._cmdFinishedDict[cmd] = True

    def _endParallel(self, interrupted):
        for cmd in self.cmdList:
            if(not self._cmdFinishedDict[cmd]):
                # End all unfinished commands
                print(f"[Auto] Ending {cmd.getName()}")
                cmd.end(interrupted)

    def _isDoneParallel(self):
        # We're done when every command has finished
        return all(self._cmdFinishedDict.values())
    
    ##################################################
    ## Sequential group operation

    def _initSequential(self):
        self._curCmdIdx = 0
        if(self._curCmdIdx < len(self.cmdList)):
            # Init the first command
            curCmd = self.cmdList[self._curCmdIdx]
            print(f"[Auto] Init {curCmd.getName()}")
            curCmd.initialize()

    def _executeSequential(self):
        if(self._curCmdIdx < len(self.cmdList)):
            # If we've got a valid command, execute it
            curCmd = self.cmdList[self._curCmdIdx]
            curCmd.execute()
            
            if(curCmd.isDone()):
                # Time to move on to the next command
                # First, Naturally end the current command
                print(f"[Auto] Ending {curCmd.getName()}")
                curCmd.end(False)
                # Move onto the next command
                self._curCmdIdx += 1
                # Init it if it exists
                if(self._curCmdIdx < len(self.cmdList)):
                    curCmd = self.cmdList[self._curCmdIdx]
                    print(f"[Auto] Init {curCmd.getName()}")
                    curCmd.initialize()
                    # That's it, next loop we'll execute it.

    def _endSequential(self, interrupted):
        # Only need to end the current command
        if(self._curCmdIdx < len(self.cmdList)):
            curCmd = self.cmdList[self._curCmdIdx]
            print(f"[Auto] Ending {curCmd.getName()}")
            curCmd.end(interrupted)

    def _isDoneSequential(self):
        # We're done when we hit the end of the list
        return self._curCmdIdx >= len(self.cmdList)

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
            

    
            