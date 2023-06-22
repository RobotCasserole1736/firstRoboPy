

from AutoSequencerV2.autoSequencer import *
from AutoSequencerV2.command import Command
from AutoSequencerV2.commandGroup import CommandGroup, GroupType


class TestCommand(Command):
    def initialize(self):
        self.execCount = 0
    def execute(self):
        self.execCount += 1
    def isDone(self):
        return ( self.execCount >= 2 or self.execCount  < 0)
    def end(self, interrupted):
        self.execCount = -1


def test_topLevel():
    autosequener_updateMode()
    autosequener_initiaize()
    autosequener_update()
    autosequener_end()



def test_parallel():
    dut = TestCommand().alongWith(TestCommand().alongWith(TestCommand()))
    
    assert isinstance(dut, CommandGroup)
    assert dut.groupType == GroupType.PARALLEL
    assert len(dut.cmdList) == 3
    for cmd in dut.cmdList:
        assert isinstance(cmd, Command)
    
    dut.initialize()
    
    for cmd in dut.cmdList:
        assert cmd.execCount == 0

    dut.execute()
    
    for cmd in dut.cmdList:
        assert cmd.execCount == 1
        
    dut.execute()
    
    for cmd in dut.cmdList:
        assert cmd.isDone()
        
    dut.end(False)
    
    # Now all commands should be ended
    for cmd in dut.cmdList:
        assert cmd.execCount == -1
        
def test_sequential():
    dut = TestCommand().andThen(TestCommand().andThen(TestCommand()))
    
    assert isinstance(dut, CommandGroup)
    assert dut.groupType == GroupType.SEQUENTIAL
    assert len(dut.cmdList) == 3
    for cmd in dut.cmdList:
        assert isinstance(cmd, Command)
    
    dut.initialize()
    
    #Check for init in the first command
    assert dut.cmdList[0].execCount == 0

    dut.execute()
    dut.execute()

    assert dut.cmdList[0].execCount == -1    
    assert dut.cmdList[1].execCount == 0

    dut.execute()
    dut.execute()
    
    assert dut.cmdList[1].execCount == -1    
    assert dut.cmdList[2].execCount == 0
        
    dut.execute()
    dut.execute()
        
    for cmd in dut.cmdList:
        assert cmd.isDone()


def test_race():
    dut = TestCommand().raceWith(TestCommand().raceWith(TestCommand()))
    
    assert isinstance(dut, CommandGroup)
    assert dut.groupType == GroupType.RACE
    assert len(dut.cmdList) == 3
    
    dut.initialize()
    
    for cmd in dut.cmdList:
        assert isinstance(cmd, Command)
        assert cmd.execCount == 0

    dut.execute()
    
    for cmd in dut.cmdList:
        assert cmd.execCount == 1
        
    dut.execute()
    
    # First command should have finished first
    assert dut.cmdList[0].isDone()
    assert not dut.cmdList[1].isDone()
    assert not dut.cmdList[2].isDone()
    
    dut.end(False)
    
    # Now all commands should be ended
    for cmd in dut.cmdList:
        assert cmd.execCount == -1