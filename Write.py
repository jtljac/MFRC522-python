import RPi.GPIO as GPIO
import EasyMFRC522

reader = EasyMFRC522.EasyMFRC522()

sector = int(input("Enter sector to write to: "))
data = raw_input("Enter data to write: ")
reader.write(data, sector)
reader.read(sector)
