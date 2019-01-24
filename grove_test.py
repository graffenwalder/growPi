
# GrovePi + Grove Ultrasonic Ranger

from grovepi import *
import time

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

potHeight = 12
sensorHeight = 73

distSensor = 6

def calcPlantHeight():
    return sensorHeight - potHeight - distValue


while True:
    try:
        distValue = ultrasonicRead(distSensor)
        # Read distance value from Ultrasonic
        print(calcPlantHeight())
        time.sleep(1)
        

    except TypeError:
        print "Error"
    except IOError:
        print "Error"