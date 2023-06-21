
# TODO - make a new abstract simple class defining the compoisiont operators

# TODO - implement the composition operators here for commands composed with groups

from AutoSequencerV2.commandParallelGroup import CommandParallelGroup
from AutoSequencerV2.commandRaceGroup import CommandRaceGroup
from AutoSequencerV2.commandSequentialGroup import CommandSequentialGroup
from AutoSequencerV2.composer import Composer
from AutoSequencerV2.runnable import Runnable


class Command(Runnable, Composer):
    
    def andThen(self, other):
        cmds = [self, other]
        return CommandSequentialGroup(cmds)
    
    def raceWith(self, other):
        cmds = [self, other]
        return CommandRaceGroup(cmds)

    def alongWith(self, other):
        cmds = [self,other]
        return CommandParallelGroup(cmds)
    