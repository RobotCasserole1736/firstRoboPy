from AutoSequencerV2.commandGroup import CommandGroup, GroupType
from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable

# A command is the basic unit of an autonomous mode
# Commands are composed together into CommandGroups
# Commands are runnable for a finite period of time - they've got init, execute (periodic), and end methods
# Users should extend the Command class to add their own functionality to these init/execute/end methods
class Command(Runnable, Composer):
    
    def andThen(self, other):
        return self._composeWith(other, GroupType.SEQUENTIAL)
    
    def raceWith(self, other):
        return self._composeWith(other, GroupType.RACE)

    def alongWith(self, other):
        return self._composeWith(other, GroupType.PARALLEL)

    def _composeWith(self, other, outputGroupType):
        if(isinstance(other, CommandGroup) and other.groupType == outputGroupType):
            cmds = [self]
            cmds.extend(other.cmdList)
        else:
            cmds = [self, other]
        return CommandGroup(cmds, outputGroupType)
    
    def getName(self):
        return self.__class__.__qualname__