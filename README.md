# growPi

Raspberry pi, with GrovePi+. Currently has Moisture, Temperature, Humidity and LightSensor.
Data is saved to temp.csv.

![growPi](/images/plantsense.jpg)  

## Setup

Attach GrovePi+ to Raspberry pi
In CLI:
```
sudo curl -kL dexterindustries.com/update_grovepi | bash
```
After reboot for changes to take effect.
See [GrovePi Setup](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/) for more.

## Hardware

#### Components:
- Raspberry Pi 3B+
  - Adapter
  - 8GB SD Card
- GrovePi+
  - Moisture Sensor
  - Light Sensor
  - LED Red (5mm)
  - Temperature & Humidity Sensor (DHT11)
  - Ultrasonic Ranger
  - LCD RGB Backlight
- Optional:
  - Heatsink for Raspberry Pi

#### Connections:
- Moisture Sensor to A0
- Light Sensor to A1
- LED Red to D3
- Temperature & Humidity Sensor to D4
- Ultrasonic Ranger to D6
- LCD RGB Backlight to IC2

Feel free to use different connections, just be sure to change them in `growpi.py`.

Finaly run `python growpi.py`

## ToDoList

- [x] Base script
- [x] Add Sensors: Moisture, Temperature, Humidity, Light
- [x] Add red led as indicator for low moisture
- [x] Add display, that displays current data
- [x] Save sensordata to csv file
- [ ] Add waterpump
- [ ] Write watering logic
- [ ] Get stable sensor data from ultrasonic reader
- [ ] Write lamp highering logic
- [ ] Make Webapp/site that auto updates with sensordata
- [ ] Add Jupyter notebook for EDA if interesting
- [x] Should really change ledmoist.py filename
