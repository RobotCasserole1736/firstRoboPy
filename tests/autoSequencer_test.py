


from AutoSequencerV2.commandSequentialGroup import CommandSequentialGroup
from AutoSequencerV2.autoSequencer import AutoSequencer


class TestCommand(Command):
    def initalize(self):
        self.execCount = 0
    def execute(self):
        self.execCount += 1


def test_topLevel():
    dut = AutoSequencer()


def test_sequential():
    dut = TestCommand().andThen(TestCommand().andThen(TestCommand()))
    
    assert(isinstance(dut, CommandSequentialGroup))
    assert(len(dut.cmdList) == 3)

