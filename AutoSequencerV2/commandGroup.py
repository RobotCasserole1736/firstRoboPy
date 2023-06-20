
from AutoSequencerV2.command import Command
from AutoSequencerV2.commandParallelGroup import CommandParallelGroup
from AutoSequencerV2.commandRaceGroup import CommandRaceGroup
from AutoSequencerV2.commandSequentialGroup import CommandSequentialGroup

# TODO make a new enum-ish class to define the style of group (Parallel, Race, Sequential)

# TODO - pull all the guts of the specific groups into here, and switch based on group type. Also, implement the composition methods here for groups composed with groups for all combos of group types

class CommandGroup(Command):
    def __init__(self, cmdList):
        self.cmdList = cmdList
        
    # Default group init - just init each command
    def initialize(self):
        for cmd in self.cmdList:
            cmd.initialize()
            
    # Default group end - end everything with same interrupted status
    def end(self, interrupted):
        for cmd in self.cmdList:
            cmd.end(interrupted)

    
            