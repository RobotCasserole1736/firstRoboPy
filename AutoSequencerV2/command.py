from abc import ABC, abstractmethod

# TODO - make a new abstract simple class defining the compoisiont operators

# TODO - implement the composition operators here for commands composed with groups

class Command(ABC):
    
        
    def execute(self):
        pass
    
    def initialize(self):
        pass
    
    def end(self, interrupted):
        pass
    
    def isDone(self):
        return False
    
    def getName(self):
        return self.__qualname__
          
    @abstractmethod
    def andThen(self, other):
        pass
    
    @abstractmethod
    def raceWith(self, other):
        pass
    
    @abstractmethod
    def alongWith(self, other):
        pass