import time
import math
import os
import csv

from grovepi import *
from grove_rgb_lcd import *

# Connect the Grove Moisture Sensor to analog port A0, Light Sensor to A1, Display to IC2
# Connect Red Led to D3, Temp Sensor to D4, UltrasonicRanger to D6

# Sensors
moistSensor = 0
lightSensor = 1
ledRed = 3
tempSensor = 4
#waterPump = 5
distSensor = 6

# Heights
potHeight = 12
sensorHeight = 73

displayInterval = 1 * 60  # How long should the display stay on?
checkInterval = 10 * 60  # How long before loop starts again?
lightThreshold = 10  # Value from where lightOn = True begins

mlSecond = 20  # How much ml water the waterpump produces per second
waterAmount = 500  # How much ml water should be given to the plants


# Write data to csv
def appendCSV():
    fields = ['Time', 'Temperature', 'Humidity', 'MoistValue', 'MoistClass',
              'LightValue', 'Lights', 'PiTemperature', 'Height', 'SonicDistance']

    with open(r'temp.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({'Time': currentTime,
                         'Temperature': temp,
                         'Humidity': humidity,
                         'MoistValue': moist,
                         'MoistClass': moistClass,
                         'LightValue': lightValue,
                         'Lights': lightsOn,
                         'PiTemperature': (measurePi()),
                         'Height': (calcPlantHeight()),
                         'SonicDistance': distValue
                         })


def calcPlantHeight():
    return sensorHeight - potHeight - distValue


def displayText():
    setRGB(0, 128, 64)  # background color led display
    text = str(temp) + "C " + str(humidity) + "% " + str(measurePi() +
                                                         "\n" + str(moist) + " " + moistClass + " " + str(lightValue) + " on")
    setText(text)
    time.sleep(displayInterval)
    setText("")
    setRGB(0, 0, 0)


def measurePi():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=", "")[0:4])


def moistClassifier():
    if moist < 300:
        moistResult = 'Dry'
    elif moist < 600:
        moistResult = 'Moist'
    else:
        moistResult = 'Wet'      
    return moistResult


def printSensorData():
    print(currentTime)
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        print("Temperature: {}'C\nHumidity: {}%".format(temp, humidity))
    else:
        print("Couldn't get temperature/humidity sensor readings")

    print('Moisture: {0} ({1})'.format(moist, moistClass))
    print("Lights: {} ({})".format(lightValue, "On" if lightsOn else "Off"))
    print("Height: {} cm".format(calcPlantHeight()))
    print("Raspberry pi: {}'C\n".format(measurePi()))


def waterPlants():
    digitalwrite(waterPump, 1)
    time.sleep(waterAmount / mlSecond)
    digitalwrite(waterPump, 0)
    print("Watering complete at: " + time.ctime())


# Main Loop
while True:
    try:
        # Time loop
        t0 = time.time()
        
        # Get sensor readings
        lightValue = analogRead(lightSensor)
        distValue = ultrasonicRead(distSensor)
        moist = analogRead(moistSensor)
        [temp, humidity] = dht(tempSensor, 0)
        
        currentTime = time.ctime()
        moistClass = moistClassifier()
        lightsOn = lightValue > lightThreshold
        
        printSensorData()
        appendCSV()
        
        # Lights on
        if lightsOn:
            # Turn on red LED when ground is dry, but only when lights are on
            digitalWrite(ledRed, 1) if moistClass == 'Dry' else digitalWrite(ledRed, 0)

            displayText()

        # Lights off
        else:
            # In case ground was dry, when lights were still on
            digitalWrite(ledRed, 0)
        
        loopTime = time.time() - t0
        time.sleep(checkInterval - loopTime)

    except KeyboardInterrupt:
        digitalWrite(ledRed, 0)
        setText("")
        setRGB(0, 0, 0)
        print("Leds and RGB shutdown safely")
        break
    except IOError:
        print("Error")



