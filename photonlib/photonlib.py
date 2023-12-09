from wpimath.geometry import Transform3d
from enum import Enum
import ntcore
from wpilib import Timer
from photonlib.packet import Packet

class TargetCorner:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y


class PhotonTrackedTarget:

    _MAX_CORNERS = 8
    _NUM_BYTES_IN_FLOAT = 8
    _PACK_SIZE_BYTES = _NUM_BYTES_IN_FLOAT * (5 + 7 + 2 * 4 + 1 + 7 + 2 * _MAX_CORNERS)

    def __init__(self, yaw:float=0, pitch:float=0, area:float=0, skew:float=0, 
                 id:int=0, pose:Transform3d=Transform3d(), altPose: Transform3d=Transform3d(), 
                 ambiguity:float=0, 
                 minAreaRectCorners: list[TargetCorner]|None = None, 
                 detectedCorners: list[TargetCorner]|None = None):
        self.yaw = yaw
        self.pitch = pitch
        self.area = area
        self.skew = skew
        self.fiducialId  = id
        self.bestCameraToTarget  = pose
        self.altCameraToTarget  = altPose
        self.minAreaRectCorners = minAreaRectCorners
        self.detectedCorners = detectedCorners
        self.poseAmbiguity = ambiguity

    def getYaw(self) -> float:
        return self.yaw
    
    def getPitch(self) -> float:
        return self.pitch
    
    def getArea(self) -> float:
        return self.area
    
    def getSkew(self) -> float:
        return self.skew
    
    def getFiducialID(self) -> int:
        return self.fiducialId
    
    def getPoseAmbiguity(self) -> float:
        return self.poseAmbiguity
    
    def getMinAreaRectCorners(self) -> list[TargetCorner]|None:
        return self.minAreaRectCorners
    
    def getDetectedCorners(self) -> list[TargetCorner]|None:
        return self.detectedCorners
    
    def _decodeTargetList(self, packet:Packet, numTargets:int) -> list[TargetCorner]:
        retList = []
        for _ in range(numTargets):
            cx = packet.decodeDouble()
            cy = packet.decodeDouble()
            retList.append(TargetCorner(cx, cy))
        return retList

    def createFromPacket(self, packet:Packet) -> Packet:
        self.yaw = packet.decodeDouble()
        self.pitch = packet.decodeDouble()
        self.area = packet.decodeDouble()
        self.skew = packet.decodeDouble()
        self.fiducialId = packet.decode16()

        self.bestCameraToTarget = packet.decodeTransform()
        self.altCameraToTarget  = packet.decodeTransform()
        self.poseAmbiguity = packet.decodeBoolean()

        self.minAreaRectCorners = self._decodeTargetList(packet, 4) # always four
        numCorners = packet.decode8()
        self.detectedCorners = self._decodeTargetList(packet, numCorners)
        return packet
    
    def __str__(self) -> str:
        return f"PhotonTrackedTarget{{yaw={self.yaw},pitch={self.pitch},area={self.area},skew={self.skew},fiducialId={self.fiducialId},bestCameraToTarget={self.bestCameraToTarget}}}"


class PhotonPipelineResult:
    def __init__(self, latencyMillis:float = -1, targets:list[PhotonTrackedTarget]|None = None):
        self.latencyMillis = latencyMillis
        self.timestampSec = Timer.getFPGATimestamp() - self.latencyMillis / 1e-3
        self.targets = targets
        self.multiTagResult = None
        
    def populateFromPacket(self, packet:Packet) -> Packet:
        self.targets = []
        self.latencyMillis = packet.decodeDouble()
        self.multiTagResult = None # TODO Decode from packet
        targetCount = packet.decode8()
        for _ in range(targetCount):
            target = PhotonTrackedTarget()
            target.createFromPacket(packet)
            self.targets.append(target)

        return packet
    
    def setTimestampSeconds(self, timestampSec:float) -> None:
        self.timestampSec = timestampSec
        
    def getLatenyMillis(self) -> float:
        return self.latencyMillis

class VisionLEDMode(Enum):
    kDefault = -1
    kOff = 0
    kOn = 1
    kBlink = 2

class PhotonCamera:
    def __init__(self, cameraName:str):
        instance = ntcore.NetworkTableInstance.getDefault()
        self.name = cameraName
        photonvision_root_table = instance.getTable("photonvision")
        cameraTable = photonvision_root_table.getSubTable(cameraName)
        self.path = cameraTable.getPath()
        self.rawBytesEntry = cameraTable.getRawTopic("rawBytes") \
                        .subscribe("rawBytes", bytes([]), ntcore.PubSubOptions(periodic=0.01, sendAll=True))
                        
        self.driverModePublisher = cameraTable.getBooleanTopic("driverModeRequest").publish()
        self.driverModeSubscriber = cameraTable.getBooleanTopic("driverMode").subscribe(False)
        self.inputSaveImgEntry = cameraTable.getIntegerTopic("inputSaveImgCmd").getEntry(0)
        self.outputSaveImgEntry = cameraTable.getIntegerTopic("outputSaveImgCmd").getEntry(0)
        self.pipelineIndexRequest = cameraTable.getIntegerTopic("pipelineIndexRequest").publish()
        self.pipelineIndexState = cameraTable.getIntegerTopic("pipelineIndexState").subscribe(0)
        self.heartbeatEntry = cameraTable.getIntegerTopic("heartbeat").subscribe(-1)

        self.ledModeRequest = photonvision_root_table.getIntegerTopic("ledModeRequest").publish()
        self.ledModeState = photonvision_root_table.getIntegerTopic("ledModeState").subscribe(-1)
        self.versionEntry = photonvision_root_table.getStringTopic("version").subscribe("")

        # Existing is enough to make this multisubscriber do its thing
        self.topicNameSubscriber = \
                ntcore.MultiSubscriber( \
                        instance, ["/photonvision/"], ntcore.PubSubOptions(topicsOnly =True))   
                
        self.prevHeartbeat = 0
        self.prevHeartbeatChangeTime = Timer.getFPGATimestamp()
                
                
    def getLatestResult(self) -> PhotonPipelineResult:
        retVal = PhotonPipelineResult()
        packetWithTimestamp = self.rawBytesEntry.getAtomic()
        byteList = packetWithTimestamp.value
        timestamp = packetWithTimestamp.time
        
        if(len(byteList) < 1):
            return retVal
        else:
            retVal.populateFromPacket(Packet(byteList))
            # NT4 allows us to correct the timestamp based on when the message was sent
            retVal.setTimestampSeconds(timestamp / 1e-6 - retVal.getLatenyMillis() / 1e-3)
            return retVal
    
    def getDriverMode(self) -> bool:
        return self.driverModeSubscriber.get()
    
    def setDriverMode(self, driverMode:bool) -> None:
        self.driverModePublisher.set(driverMode)
    
    def takeInputSnapshot(self) -> None:
        self.inputSaveImgEntry.set(self.inputSaveImgEntry.get() + 1)
   
    def takeOutputSnapshot(self) -> None:
        self.outputSaveImgEntry.set(self.outputSaveImgEntry.get() + 1)
    
    def getPipelineIndex(self) -> int:
        return self.pipelineIndexState.get(0)

    def setPipelineIndex(self, index:int) -> None:
        self.pipelineIndexRequest.set(index)
    
    def getLEDMode(self) -> VisionLEDMode:
        mode = self.ledModeState.get()
        return VisionLEDMode(mode)
    
    def setLEDMode(self, led:VisionLEDMode) -> None:
        self.ledModeRequest.set(led.value)
    
    def getName(self) -> str:
        return self.name
    
    def isConnected(self) -> bool:
        curHeartbeat = self.heartbeatEntry.get()
        now = Timer.getFPGATimestamp()
        
        if(curHeartbeat != self.prevHeartbeat):
            self.prevHeartbeat = curHeartbeat
            self.prevHeartbeatChangeTime = now
            
        return (now - self.prevHeartbeatChangeTime) < 0.5