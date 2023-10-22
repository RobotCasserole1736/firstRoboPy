
# Abstract class defining the methods that any command or command group which 
# whishes to participate in a _composition_ must support


class Composer():

    def _optimizeCmdList(self, first,second, outType):
        from AutoSequencerV2.command import Command # pylint: disable=import-outside-toplevel

        if(isinstance(first, outType) and isinstance(second,outType)):
            #They're both the same type - optimize to a single command list
            cmds = []
            cmds.extend(first.cmdList)
            cmds.extend(second.cmdList)
        elif(isinstance(first, outType) and isinstance(second, Command)):
            cmds = []
            cmds.extend(first.cmdList)
            cmds.append(second)
        elif(isinstance(first, Command) and isinstance(second, outType)):
            cmds = []
            cmds.append(first)
            cmds.extend(second.cmdList)
        else:
            cmds = [first,second]
        return cmds

    def andThen(self, other):
        from .sequentialCommandGroup import SequentialCommandGroup # pylint: disable=import-outside-toplevel

        cmds = self._optimizeCmdList(self, other, SequentialCommandGroup)

        return SequentialCommandGroup(cmds)
    
    def raceWith(self, other):
        from .raceCommandGroup import RaceCommandGroup # pylint: disable=import-outside-toplevel
        
        cmds = self._optimizeCmdList(self, other, RaceCommandGroup)

        return RaceCommandGroup(cmds)
    
    def alongWith(self, other):
        from .parallelCommandGroup import ParallelCommandGroup # pylint: disable=import-outside-toplevel

        cmds = self._optimizeCmdList(self, other, ParallelCommandGroup)

        return ParallelCommandGroup(cmds)