# growPi

Raspberry pi, with GrovePi+ to read plant data. Data is saved to `temp.csv`. Takes a picture on every interval.
If moisture readings are "Dry" for 3 consecutive intervals, the waterpump will activate.

Current sensors: moisture, light, temperature, humidity and distance.

![growPi](/images/plantsense.jpg)

## Hardware

- Raspberry Pi 3B+
  - Adapter
  - 32GB SD Card (8GB is enough when not using camera)
- GrovePi+
  - [Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)
  - [Light Sensor](http://wiki.seeedstudio.com/Grove-Light_Sensor/)
  - [LED Red (5mm)](http://wiki.seeedstudio.com/Grove-Red_LED/)
  - [Temperature & Humidity Sensor (DHT22)](http://wiki.seeedstudio.com/Grove-Temperature_and_Humidity_Sensor_Pro/)
  - [Ultrasonic Ranger](http://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
  - [LCD RGB Backlight](http://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/)
  - [Mini Fan](http://wiki.seeedstudio.com/Grove-Mini_Fan/)
- [3-6V Waterpump](https://www.bitsandparts.eu/Motoren-Servos-and-Drivers/Doseringspomp-Waterpomp-dompelpomp-3-6V-120l-h/p116339)
  - Aquarium tubing
  - Watercontainer (bottle, bucket.....)
  - 2 female to female jumper wires
- Optional:
  - Heatsink for Raspberry Pi
  - Raspberry Pi Camera (Board V2 - 8MP)

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
6. Connect waterpump to Mini Fan board:
- Carefully take off the plastic shell of both the jumperwires, on one end.
- Pull the waterpump wires through the small holes of the shells.
- Put the waterpump wires in the stripped opening of the jumperwires and attach them with some plyers
- Pull back the shells.
- Attach the other end of the jumperwires to the Mini Fan board, where the Mini Fan plug normaly goes.
- Attach aquarium tubing and put in watercontainer.
![waterpump](/images/waterpump.jpg)
7. Connect sensors to the GrovePi ports:

| Module/Sensor                  | Port  | 
| -------------------------------|-------|
| Moisture Sensor                | A0    |
| Light Sensor                   | A1    |
| Mini Fan board (waterpump)	 | D2	 |
| LED Red                        | D3    |
| Temperature & Humidity Sensor  | D4    |
| Ultrasonic Ranger              | D6    |
| LCD RGB Backlight              | IC2   |

Feel free to use different ports, just be sure to change them in `growpi.py`.

8. Launch growPi:
```
$ python growpi.py
```

## ToDoList

- [x] Base script
- [x] Add Sensors: Moisture, Temperature, Humidity, Light
- [x] Add red led as indicator for low moisture
- [x] Add display, that displays current data
- [x] Save sensordata to csv file
- [x] Add camera
- [x] Add waterpump
- [x] Write watering logic
- [x] Write waterpump setup
- [ ] Get stable sensor data from Ultrasonic Ranger
- [ ] Make Webapp/site that auto updates with sensordata
- [ ] Add Jupyter notebook with EDA if interesting
- [x] Should really change ledmoist.py filename

## Notes

- The waterpump in this setup produces about 5ml/second. Make sure to test how much your setup produces, results may vary.