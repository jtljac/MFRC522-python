import RPi.GPIO as GPIO
import EasyMFRC522

reader = EasyMFRC522.EasyMFRC522()
sector = int(input("Enter sector to visit: "))
print(reader.read(sector))
