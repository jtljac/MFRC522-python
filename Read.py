import RPi.GPIO as GPIO
import EasyMFRC522

reader = EasyMFRC522.EasyMFRC522()

print(reader.read(int(input("Enter sector to visit: "))))
