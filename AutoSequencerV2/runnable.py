        
class Runnable():
    
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