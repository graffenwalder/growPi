# growPi

Raspberry pi, with GrovePi+ to read plant data. Data is saved to `temp.csv`.

Current sensors attached: moisture, light, temperature, humidity and distance.

![growPi](/images/plantsense.jpg)

## Hardware

- Raspberry Pi 3B+
  - Adapter
  - 8GB SD Card
- GrovePi+
  - [Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)
  - [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  - [LED Red (5mm)](http://wiki.seeedstudio.com/Grove-Red_LED/)
  - [Temperature & Humidity Sensor (DHT11)](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
  - [Ultrasonic Ranger](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
  - [LCD RGB Backlight](http://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/)
- Optional:
  - Heatsink for Raspberry Pi

## Setup

1. Download and burn [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) to SD card.
2. Do initial Raspbian setup, make sure to setup an internet connection.
3. Update Raspbian:
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get dist-upgrade
```
4. Attach GrovePi+ To Raspberry Pi and run:
```
$ sudo curl -kL dexterindustries.com/update_grovepi | bash
$ sudo reboot
```
5. After reboot run: 
```
$ sudo i2cdetect -y 1
```
- If the install was succesfull, you should see "04" in the output.
- See [GrovePi Setup](https://www.dexterindustries.com/GrovePi/get-started-with-the-grovepi/setting-software/) if unsuccesfull.
6. Connect sensors to the GrovePi ports:

| Module/Sensor                  | Port  | 
| -------------------------------|-------|
| Moisture Sensor                | A0    |
| Light Sensor                   | A1    |
| LED Red                        | D3    |
| Temperature & Humidity Sensor  | D4    |
| Ultrasonic Ranger              | D6    |
| LCD RGB Backlight              | IC2   |

Feel free to use different ports, just be sure to change them in `growpi.py`.

7. Launch growPi:
```
$ python growpi.py
```

## ToDoList

- [x] Base script
- [x] Add Sensors: Moisture, Temperature, Humidity, Light
- [x] Add red led as indicator for low moisture
- [x] Add display, that displays current data
- [x] Save sensordata to csv file
- [ ] Add waterpump
- [ ] Write watering logic
- [ ] Get stable sensor data from Ultrasonic Ranger
- [ ] Write lamp highering logic
- [ ] Make Webapp/site that auto updates with sensordata
- [ ] Add Jupyter notebook with EDA if interesting
- [x] Should really change ledmoist.py filename