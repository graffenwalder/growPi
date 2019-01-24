import time
import math
import os
import csv

from grovepi import *
from grove_rgb_lcd import *

# Connect the Grove Moisture Sensor to analog port A0, Light Sensor to A1, Display to IC2
# Connect Red Led to D3, Temp Sensor to D4, display to 
# SIG,NC,VCC,GND
moistSensor = 0
lightSensor = 1
ledRed = 3
tempSensor = 4
#waterPump = 5
distSensor = 6

#Heights
potHeight = 12
sensorHeight = 73


displayInterval = 1 * 60 #How long should the display stay on?
checkInterval = 10 * 60# seconds between loop
lightThreshold = 10 # value at wich Light begins

mlSecond = 20 # How much mililiter the waterpump produces per second
waterAmount = 500 # How much mililiter water should be given to the plants

def displayText():
    setRGB(0,128,64) # background color led display
    text = str(temp) + "C " + str(humidity) + "% " + str(measurePi() + "\n" + str(moist) + " " + moistResult + " " + str(lightValue) + " on")
    setText(text)
    
    time.sleep(displayInterval)
    setText("") 
    setRGB(0,0,0)
    
def calcPlantHeight():
    return sensorHeight - potHeight - distValue 

def measurePi():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=","")[0:4])
    
# Write data to csv
def appendCSV():
    fields=['Time','Temperature','Humidity', 'MoistValue', 'MoistClass', 'LightValue', 'Lights', 'PiTemperature', 'Height']
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
                         'Height': (calcPlantHeight())
                         })

def waterPlants():
    #digitalWrite(ledGreen,1) # Both lights burning now, indicate watering
    digitalwrite(waterPump,1)
    time.sleep(waterAmount/mlSecond)
    digitalwrite(waterPump,0)
    print("Watering complete at: " + time.ctime())


lightsOn = True

while True:
    try:
        lightValue = analogRead(lightSensor)
        distValue = ultrasonicRead(distSensor)
        
        if lightValue <= lightThreshold:
            lightsOn = False
        else:
            lightsOn = True
            
        moist = analogRead(moistSensor)
        
        currentTime = time.ctime()
        
        if 0 <= moist and moist < 300:
            moistResult = 'Dry'
            digitalWrite(ledRed,1)
            #print("Dry ground, watering plants...")
            #waterPlants()
            
        elif 300 <= moist and moist < 600:
            moistResult = 'Moist'
            digitalWrite(ledRed,0)
            #digitalwrite(waterPump,0)
        else:
            moistResult = 'Wet'
            digitalWrite(ledRed,1)
            #digitalwrite(waterPump,0)
        
#       printStatements
        print(currentTime)
        # This example uses the blue colored sensor. = 0
        # The first parameter is the port, the second parameter is the type of sensor.
        try:
            [temp,humidity] = dht(tempSensor,0)  
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                print("Temperature: {0:.02f}'C\nHumidity: {1:.02f}%".format(temp, humidity))
#                print("Temperature: %.02f'C\nHumidity: %.02f%%"%(temp, humidity))
        except IOError:
            print ("Error")
        
        print('Moisture value: {0} ({1})'.format(moist, moistResult))
        if lightsOn:
            print("Lights: {} (On)".format(lightValue))
        else:
            print("Lights: {} (Off)".format(lightValue))
        print("Height: " + str(calcPlantHeight()) + " cm")
        print("Raspberry pi: " + measurePi() + "'C\n")
        
        
        appendCSV()
        if lightsOn:
            displayText()
            # Time to next check minus display sleep
            time.sleep(checkInterval - displayInterval)
        else:
            time.sleep(checkInterval)

    except KeyboardInterrupt:
        digitalWrite(ledRed,0)
        #digitalWrite(waterPump,0)
        setText("")
        setRGB(0,0,0)
        print("Leds and RGB shutdown safely")
        break
    except IOError:
        print ("Error")
