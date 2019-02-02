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
                         'MoistClass': moistResult,
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
                                                         "\n" + str(moist) + " " + moistResult + " " + str(lightValue) + " on")

    setText(text)
    time.sleep(displayInterval)
    setText("")
    setRGB(0, 0, 0)


def measurePi():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=", "")[0:4])


def printStatements():
    print(currentTime)
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        print("Temperature: {0:.02f}'C\nHumidity: {1:.02f}%".format(
            temp, humidity))
    else:
        print("Couldn't get temperature/humidity sensor readings")

    print('Moisture value: {0} ({1})'.format(moist, moistResult))

    if lightsOn:
        print("Lights: {} (On)".format(lightValue))
    else:
        print("Lights: {} (Off)".format(lightValue))

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
        # Get sensor readings
        lightValue = analogRead(lightSensor)
        distValue = ultrasonicRead(distSensor)
        moist = analogRead(moistSensor)
        [temp, humidity] = dht(tempSensor, 0)
        currentTime = time.ctime()

        if 0 <= moist and moist < 300:
            moistResult = 'Dry'
        elif 300 <= moist and moist < 600:
            moistResult = 'Moist'
        else:
            moistResult = 'Wet'

        # Lights on
        if lightValue > lightThreshold:
            lightsOn = True

            printStatements()
            appendCSV()

            # Turn on red LED when ground is dry, but only when lights are on
            if moistResult == 'Dry':
                digitalWrite(ledRed, 1)
            else:
                digitalWrite(ledRed, 0)

            displayText()
            # Time to next check minus display time
            time.sleep(checkInterval - displayInterval)

        # Lights off
        else:
            lightsOn = False

            printStatements()
            appendCSV()

            # In case ground was dry, when lights where still on
            digitalWrite(ledRed, 0)

            time.sleep(checkInterval)

    except KeyboardInterrupt:
        digitalWrite(ledRed, 0)
        setText("")
        setRGB(0, 0, 0)
        print("Leds and RGB shutdown safely")
        break
    except IOError:
        print("Error")

