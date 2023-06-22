from AutoSequencerV2.commandGroup import CommandGroup, GroupType
from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable


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
    