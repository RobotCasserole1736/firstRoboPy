

from AutoSequencerV2.command import Command


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
            