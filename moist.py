import time
import grovepi

# Connect the Grove Moisture Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0

while True:
    try:
        moist = grovepi.analogRead(sensor)
        if 0 <= moist and moist < 300:
            result = 'Dry'
        elif 300 <= moist and moist < 600:
            result = 'Moist'
        else:
            result = 'Wet'
        print('Moisture value: {0}, {1}'.format(moist, result))
        time.sleep(1.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")
