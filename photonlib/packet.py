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
     * Returns a decoded byte from the packet.
     *
     * @return A decoded byte from the packet.
    """
    def decodeByte(self): 
        if (len(self.packetData) < self.readPos):
            return '\0'
        
        ret = self.packetData[self.readPos]
        self.readPos += 1
        return ret
    

    """
     * Returns a decoded int from the packet.
     *
     * @return A decoded int from the packet.
    """
     int decodeInt() 
        if (len(self.data) < self.readPos + 3) 
            return 0
        
        return (0xff & self.packetData[self.readPos++]) << 24
                | (0xff & self.packetData[self.readPos++]) << 16
                | (0xff & self.packetData[self.readPos++]) << 8
                | (0xff & self.packetData[self.readPos++])
    

    """
     * Returns a decoded double from the packet.
     *
     * @return A decoded double from the packet.
    """
     double decodeDouble() 
        if (len(self.data) < (self.readPos + 7)) 
            return 0
        
        long data =
                (long) (0xff & self.packetData[self.readPos++]) << 56
                        | (long) (0xff & self.packetData[self.readPos++]) << 48
                        | (long) (0xff & self.packetData[self.readPos++]) << 40
                        | (long) (0xff & self.packetData[self.readPos++]) << 32
                        | (long) (0xff & self.packetData[self.readPos++]) << 24
                        | (long) (0xff & self.packetData[self.readPos++]) << 16
                        | (long) (0xff & self.packetData[self.readPos++]) << 8
                        | (long) (0xff & self.packetData[self.readPos++])
        return Double.longBitsToDouble(data)
    

    """
     * Returns a decoded boolean from the packet.
     *
     * @return A decoded boolean from the packet.
    """
     boolean decodeBoolean() 
        if (len(self.data) < self.readPos) 
            return false
        
        return self.packetData[self.readPos++] == 1
    

     def encode(double[] data) 
        for (double d : data) 
            encode(d)
        
    

     double[] decodeDoubleArray(int len) 
        double[] ret = new double[len]
        for (int i = 0 i < len i++) 
            ret[i] = decodeDouble()
        
        return ret
    

     short decodeShort() 
        if (len(self.data) < self.readPos + 1) 
            return 0
        
        return (short) ((0xff & self.packetData[self.readPos++]) << 8 | (0xff & self.packetData[self.readPos++]))
    
