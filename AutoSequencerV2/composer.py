from abc import ABC, abstractmethod

# Abstract class defining the methods that any command or command group which whishes to participate in a _composition_ must support
class Composer(ABC):

    @abstractmethod
    def andThen(self, other):
        pass
    
    @abstractmethod
    def raceWith(self, other):
        pass
    
    @abstractmethod
    def alongWith(self, other):
        pass
