import time
import math
import os
import csv
from grovepi import *

# Connect the Grove Moisture Sensor to analog port A0
# Connect Red led to D3, and green to D4
# SIG,NC,VCC,GND
moistSensor = 0
ledRed = 3
#ledGreen = 4
tempSensor = 4
waterPump = 5

checkInterval = 10 * 60# seconds between loop
mlSecond = 20 # How much mililiter the waterpump produces per second
waterAmount = 500 # How much mililiter water should be given to the plants

def measurePi():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

def waterPlants():
    #digitalWrite(ledGreen,1) # Both lights burning now, indicate watering
    digitalwrite(waterPump,1)
    time.sleep(waterAmount/mlSecond)
    digitalwrite(waterPump,0)
    print("Watering complete at: " + time.ctime())

while True:
    try:
        moist = analogRead(moistSensor)
        if 0 <= moist and moist < 300:
            result = 'Dry'
            digitalWrite(ledRed,1)
            #digitalWrite(ledGreen,0)
            print("Dry ground, watering plants...")
            #waterPlants()
            
            
        elif 300 <= moist and moist < 600:
            result = 'Moist'
            digitalWrite(ledRed,0)
            #digitalWrite(ledGreen,1)
            #digitalwrite(waterPump,0)
        else:
            result = 'Wet'
            digitalWrite(ledRed,1)
            #digitalWrite(ledGreen,0)
            #digitalwrite(waterPump,0)
        
        # This example uses the blue colored sensor. = 0
        # The first parameter is the port, the second parameter is the type of sensor.
        print(time.ctime())
        
        try:
            [temp,humidity] = dht(tempSensor,0)  
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                print("Temperature: %.02f'C\nHumidity: %.02f%%"%(temp, humidity))
        except IOError:
            print ("Error")
        
        print('Moisture value: {0} ({1})'.format(moist, result))
        print("Raspberry pi: " + measurePi())
        
        fields=['Time','Temperature','Humidity', 'MoistValue', 'MoistClass', 'PiTemperature' ]
        with open(r'temp.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow({'Time': time.ctime(),
                             'Temperature': temp,
                             'Humidity': humidity,
                             'MoistValue': moist,
                             'MoistClass': result,
                             'PiTemperature': (measurePi())[0:4]
                             })
            
        time.sleep(checkInterval)

    except KeyboardInterrupt:
        digitalWrite(ledRed,0)
        #digitalWrite(ledGreen,0)
        #digitalWrite(waterPump,0)
        print("Leds and pump shutdown safely")
        break
    except IOError:
        print ("Error")
