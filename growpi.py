import csv
import math
import os
import picamera
import time

from grovepi import *
from grove_rgb_lcd import *

# Connect the Grove Moisture Sensor to analog port A0, Light Sensor to A1, Display to IC2
# Connect Red Led to D3, Temp Sensor to D4, UltrasonicRanger to D6

# Sensors
moistureSensor = 0
lightSensor = 1
ledRed = 3
tempSensor = 4
#waterPump = 5
distanceSensor = 6

# Heights
potHeight = 12
sensorHeight = 73

displayInterval = 1 * 60  # How long should the display stay on?
checkInterval = 10 * 60  # How long before loop starts again?
lightThreshold = 10  # Value above threshold is lightsOn

mlSecond = 20  # How much ml water the waterpump produces per second
waterAmount = 500  # How much ml water should be given to the plants


# Write data to csv
def appendCSV():
    fields = ['Time', 'Temperature', 'Humidity', 'Moisture', 'MoistureClass',
              'LightValue', 'Lights', 'PiTemperature', 'Height', 'SonicDistance', 'ImagePath']

    with open(r'temp.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow({'Time': currentTime,
                         'Temperature': temp,
                         'Humidity': humidity,
                         'Moisture': moisture,
                         'MoistureClass': moistureClass,
                         'LightValue': lightValue,
                         'Lights': lightsOn,
                         'PiTemperature': (piTemperature()),
                         'Height': (calcPlantHeight()),
                         'SonicDistance': ultraSonicDistance,
                         'ImagePath': image
                         })


def calcPlantHeight():
    return sensorHeight - potHeight - ultraSonicDistance


def displayText():
    setRGB(0, 128, 64)  # background color led display
    setText("{}C {}% {}\n{} ({}) {}".format(temp, humidity, piTemperature(), moisture, moistureClass, lightValue))
    time.sleep(displayInterval)
    setText("")
    setRGB(0, 0, 0)


def piTemperature():
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp[5:9]


def moistureClassifier():
    if moisture < 300:
        moistureResult = 'Dry'
    elif moisture < 600:
        moistureResult = 'Moist'
    else:
        moistureResult = 'Wet'
    return moistureResult


def printSensorData():
    print(currentTime)
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        print("Temperature: {}'C\nHumidity: {}%".format(temp, humidity))
    else:
        print("Couldn't get temperature/humidity sensor readings")

    print('Moisture: {0} ({1})'.format(moisture, moistureClass))
    print("Lights: {} ({})".format(lightValue, "On" if lightsOn else "Off"))
    print("Height: {} cm".format(calcPlantHeight()))
    print("Raspberry pi: {}'C".format(piTemperature()))
    if lightsOn:
        print("Image location: {}\n".format(image))
    else:
        print("")


def takePicture():
    timestamp = time.strftime("%Y-%m-%d--%H-%M")
    imagePath = '/home/pi/Desktop/images/{}.jpg'.format(timestamp)
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.awb_mode = 'sunlight'
        time.sleep(5)
        camera.capture(imagePath)
        camera.stop_preview()
    return imagePath


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
        ultraSonicDistance = ultrasonicRead(distanceSensor)
        moisture = analogRead(moistureSensor)
        [temp, humidity] = dht(tempSensor, 0)

        currentTime = time.ctime()
        moistureClass = moistureClassifier()
        lightsOn = lightValue > lightThreshold

        # Lights on
        if lightsOn:
            # Turn on red LED when ground is dry, when lightsOn
            digitalWrite(ledRed, 1) if moistureClass == 'Dry' else digitalWrite(ledRed, 0)

            # Take picture every loop, while lightsOn, store path in image variable
            image = takePicture()

            # PrintSensorData and appendCSV, before displayText
            printSensorData()
            appendCSV()

            # Textdisplay when lightsOn
            displayText()

        # Lights off
        else:
            # In case ground was dry, when lightsOn
            digitalWrite(ledRed, 0)
            
            # No picture when lights off, empty string for appendCSV
            image = ''

            printSensorData()
            appendCSV()

        loopTime = time.time() - t0
        time.sleep(checkInterval - loopTime)

    except KeyboardInterrupt:
        digitalWrite(ledRed, 0)
        setText("")
        setRGB(0, 0, 0)
        print(" Leds and RGB shutdown safely")
        break
    except IOError:
        print("Error")
