
# GrovePi + Grove Ultrasonic Ranger

from grovepi import *
from grove_rgb_lcd import *

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

ultrasonic_ranger = 4
setRGB(0,128,64)

while True:
    try:
        # Read distance value from Ultrasonic
        text = str(ultrasonicRead(ultrasonic_ranger))
        setText(text)
        time.sleep(0.5)
        # print ultrasonicRead(ultrasonic_ranger)

    except TypeError:
        print "Error"
    except IOError:
        print "Error"
    except KeyboardInterrupt:
        exit()

