import wpilib
from enum import Enum


class PhotonPipelineResult:
    pass #TODO

class VisionLEDMode(Enum):
    kDefault = -1
    kOff = 0
    kOn = 1
    kBlink = 2

class PhotonCamera:
    def __init__(self, cameraName:str):
        pass #TODO
    
    def getLatestResult(self) -> PhotonPipelineResult:
        pass #todo
    
    def getDriverMode(self) -> bool:
        pass # TODO
    
    def setDriverMode(self, driverMode:bool) -> None:
        pass # TODO
    
    def takeInputSnapshot(self) -> None:
        pass # TODO
   
    def takeOutputSnapshot(self) -> None:
        pass # TODO 
    
    def getPipelineIndex(self) -> int:
        pass # TODO

    def setPipelineIndex(self, index:int) -> None:
        pass # TODO
    
    def getLEDMode(self) -> VisionLEDMode:
        pass # TODO
    
    def setLEDMode(self, led:VisionLEDMode) -> None:
        pass # TODO
    
    def getName(self) -> str:
        pass # TODO
    
    def isConnected(self) -> bool:
        pass # TODO