import MFRC522
import RPi.GPIO as GPIO

class EasyMFRC522:
    pointer = None
    key = None
    numSectors = 16
    numBlocks = 4

    def __init__(self, key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]):
        self.key = key

        self.pointer = MFRC522.MFRC522()

    def read(self, sector):
        if sector > 15:
            print("inaccessable sector")
            return None, None
        id, text = self.nonBlockingRead(sector)
        while not id:
            id, text = self.nonBlockingRead(sector)
        return id, text
    
    def readID(self):
        gotID = False
        while not gotID:
            gotID, id = self.connect()
        return id
    
    def nonBlockingRead(self, sector):
        connected, id = self.connect()
        if not connected:
            return None, None
        
        status = self.pointer.MFRC522_Auth(self.pointer.PICC_AUTHENT1A, sector*4 + 3, self.key, uid)
        if status != self.pointer.MI_OK:
            return None, None
        data = []
        for i in range(0,2):
            toRead = sector*4 + i
            data.append(self.pointer.MFRC522_Read(toRead))
        
        if not data and not data[0]:
            return None, None
        print(data)
        text = ""
        for items in data:
            for item in items:
                text += chr(item)
        
        self.pointer.MFRC522_StopCrypto1()
        return id, text.strip(" ")
    
    def readBlock(self, block):
        if block > 63:
            print("inaccessable block")
            return None, None
        id, text = self.nonBlockingReadBlock(block)
        while not id:
            id, text = self.nonBlockingReadBlock(block)
        return id, text
    
    def nonBlockingReadBlock(self, block):
        connected, id = self.connect()
        if not connected:
            return None, None
        
        status = self.pointer.MFRC522_Auth(self.pointer.PICC_AUTHENT1A, (block // 4)*4 + 3, self.key, uid)
        if status != self.pointer.MI_OK:
            return None, None
            data = (self.pointer.MFRC522_Read(block))
        
        if not data:
            return None, None
        print(data)
        text = ""
        for item in data:
            text += chr(item)
        
        self.pointer.MFRC522_StopCrypto1()
        return id, text.strip(" ")
    
    def write(self, text, sector):
        if len(text) > 48:
            print("Data is too large")
            return None
        data = bytearray(text.ljust(48).encode("ascii"))
        id = self.nonBlockingWrite(data, sector)
        while not id:
            id = self.nonBlockingWrite(data, sector)
        
    def nonBlockingWrite(self, data, sector):
        connected, id = self.connect()
        if not connected:
            return None, None
        
        status = self.pointer.MFRC522_Auth(self.pointer.PICC_AUTHENT1A, sector*4 + 3, self.key, uid)
        if status != self.pointer.MI_OK:
            return None
        for i in range(0,2):
            self.pointer.MFRC522_Write(sector*4 + i, data[(i*16):(i+1)*16])
        self.pointer.MFRC522_StopCrypto1()
        return id
    
    def writeBlock(self, text, block):
        if len(text) > 16:
            print("Data is too large")
            return None
        data = bytearray(text.ljust(16).encode("ascii"))
        id = self.nonBlockingWrite(data, sector)
        while not id:
            id = self.nonBlockingWrite(data, sector)
        
    def nonBlockingWriteBlock(self, data, block):
        connected, id = self.connect()
        if not connected:
            return None, None
        
        status = self.pointer.MFRC522_Auth(self.pointer.PICC_AUTHENT1A, (block//4)*4 + 3, self.key, uid)
        if status != self.pointer.MI_OK:
            return None
        self.pointer.MFRC522_Write(block, data])
        self.pointer.MFRC522_StopCrypto1()
        return id
    
    def connect(self):
        (status,TagType) = self.pointer.MFRC522_Request(self.pointer.PICC_REQIDL)
        if status != self.pointer.MI_OK:
            return False, None
        
        (status,uid) = self.pointer.MFRC522_Anticoll()
        if status != self.pointer.MI_OK:
            return False, None
        id = self.concatinateID(uid)
        self.pointer.MFRC522_SelectTag(uid)
        return True, id
        
    def concatinateID(self, ID):
        id = ""
        for item in ID:
            id += str(item) + ","
        return id.strip(",")
        
    def getSectorFromBlock(self, block):
        return block // 4
