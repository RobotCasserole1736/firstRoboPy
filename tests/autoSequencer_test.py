


from AutoSequencerV2.autoSequencer import AutoSequencer
from AutoSequencerV2.command import Command
from AutoSequencerV2.commandGroup import CommandGroup


class TestCommand(Command):
    def initalize(self):
        self.execCount = 0
    def execute(self):
        self.execCount += 1


def test_topLevel():
    dut = AutoSequencer()


def test_sequential():
    dut = TestCommand().andThen(TestCommand().andThen(TestCommand()))
    
    assert(isinstance(dut, CommandGroup))
    assert(len(dut.cmdList) == 3)

