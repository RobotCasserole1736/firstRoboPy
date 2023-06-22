from abc import ABC, abstractmethod


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
