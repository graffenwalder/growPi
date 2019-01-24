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

### Connections:
- Moisture Sensor to A0
- Light Sensor to A1
- Red led to D3
- Temperature/Humidity Sensor to D4
- Waterpump to D5
- UltraSonicRanger to D6

Feel free to use different connections, just be sure to change them in `ledmoist.py`.
Finaly run `ledmoist.py`

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
- [ ] Should really change ledmoist.py filename
