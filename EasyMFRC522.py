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
        if sector == 0 or sector > 15:
            print("inaccessable sector")
            return None, None
        id, text = self.nonBlockingRead(sector)
        while not id:
            id, text = self.nonBlockingRead(sector)
        return id, text
    
    def nonBlockingRead(self, sector):
        (status,TagType) = self.pointer.MFRC522_Request(self.pointer.PICC_REQIDL)
        if status != self.pointer.MI_OK:
            return None, None
        (status,uid) = self.pointer.MFRC522_Anticoll()
        if status != self.pointer.MI_OK:
            return None, None
        id = self.concatinateID(uid)
        
        self.pointer.MFRC522_SelectTag(uid)
        
        status = self.pointer.MFRC522_Auth(self.pointer.PICC_AUTHENT1A, sector, self.key, uid)
        if status != self.pointer.MI_OK:
            return None, None
        data = []
        for i in range(0,3):
            data.append(self.pointer.MFRC522_Read(sector*4 + i))
        self.pointer.MFRC522_StopCrypto1()
        text = ""
        for items in data:
            for item in items:
                data += chr(item)
        return id, text
        
    def concatinateID(self, ID):
        id = ""
        for item in ID:
            id += str(item) + ","
        return id.strip(",")
        
            
