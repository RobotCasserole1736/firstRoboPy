

from AutoSequencerV2.commandParallelGroup import CommandParallelGroup
from AutoSequencerV2.commandRaceGroup import CommandRaceGroup
from AutoSequencerV2.commandSequentialGroup import CommandSequentialGroup


class Command():
    
    def execute(self):
        pass
    
    def initialize(self):
        pass
    
    def end(self, interrupted):
        pass
    
    def isDone(self):
        return False
    
    def andThen(self, other):
        cmds = [self, other]
        return CommandSequentialGroup(cmds)
    
    def raceWith(self, other):
        cmds = [self, other]
        return CommandRaceGroup(cmds)
    
    def alongWith(self, other):
        cmds = [self,other]
        return CommandParallelGroup(cmds)
    
    def getName(self):
        return self.__qualname__
    