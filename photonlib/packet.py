import struct
from wpimath.geometry import Transform3d, Translation3d, Rotation3d, Quaternion

class Packet:

    """
     * Constructs an empty packet.
     *
     * @param self.size The self.size of the packet buffer.
    """
    def __init__(self, data:list[int]):
        self.packetData = data
        self.size = len(data)
        self.readPos = 0
        self.writePos = 0
    

    """ Clears the packet and resets the read and write positions."""
    def clear(self): 
        self.packetData = [0]*self.size
        self.readPos = 0
        self.writePos = 0
    

    def getSize(self): 
        return self.size
    

    """
     * Returns the packet data.
     *
     * @return The packet data.
    """
    def getData(self) -> list[int]: 
        return self.packetData
    

    """
     * Sets the packet data.
     *
     * @param data The packet data.
    """
    def setData(self, data:list[int]):
        self.packetData = data
        self.size = len(self.packetData)
    

    """
     * Returns a single decoded byte from the packet.
     *
     * @return A decoded byte from the packet.
    """
    def decode8(self) -> int: 
        if (len(self.packetData) < self.readPos):
            return 0x00
        
        ret = self.packetData[self.readPos]
        self.readPos += 1
        return ret
    

    """
     * Returns a decoded int (32 bytes) from the packet.
     *
     * @return A decoded int from the packet.
    """
    def decode32(self) -> int: 
        if (len(self.packetData) < self.readPos + 3):
            return 0x00
        
        retVal = 0x00
        retVal |= (0xff & self.packetData[self.readPos]) << 24
        self.readPos+=1
        retVal |= (0xff & self.packetData[self.readPos]) << 16
        self.readPos+=1
        retVal |= (0xff & self.packetData[self.readPos]) << 8
        self.readPos+=1
        retVal |= (0xff & self.packetData[self.readPos])
        self.readPos+=1
        return retVal
    

    """
     * Returns a decoded double from the packet.
     *
     * @return A decoded double from the packet.
    """
    def decodeDouble(self) -> float: 
        if (len(self.packetData) < (self.readPos + 7)):
            return 0

        # Read 8 ints in from the data buffer
        intList = []
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
        intList.append(0xff & self.packetData[self.readPos])
        self.readPos += 1
       
        # Interpret the bytes as a floating point number
        value = struct.unpack('d', bytes(intList))[0]

        return value
    

    """
     * Returns a decoded boolean from the packet.
     *
     * @return A decoded boolean from the packet.
    """
    def decodeBoolean(self) -> bool:
        if (len(self.packetData) < self.readPos):
            return False
        
        retVal = self.packetData[self.readPos] == 1
        self.readPos += 1
        return retVal


    def decodeDoubleArray(self, length:int) -> list[float]:
        ret = []
        for _ in range(length):
            ret.append(self.decodeDouble())
        return ret
    
    """
     * Returns a single decoded byte from the packet.
     *
     * @return A decoded byte from the packet.
    """
    def decode16(self) -> int: 
        if (len(self.packetData) < self.readPos):
            return 0x00
        
        ret = 0x00
        ret |= (self.packetData[self.readPos]) << 8
        self.readPos += 1
        ret |= self.packetData[self.readPos]
        self.readPos += 1
        return ret
    
    def decodeTransform(self) -> Transform3d:
        x = self.decodeDouble()
        y = self.decodeDouble()
        z = self.decodeDouble()
        translation = Translation3d(x,y,z)

        w = self.decodeDouble()
        x = self.decodeDouble()
        y = self.decodeDouble()
        z = self.decodeDouble()
        rotation = Rotation3d(Quaternion(w,x,y,z))

        return Transform3d(translation, rotation)

