## Installing the GrovePi for Python

This is how the GrovePi python library has to be installed:
```bash
curl -kL dexterindustries.com/update_grovepi | bash
```

You can also install it by running the `setup.py` installer, but beware of the other requirements for it too: specifically about the `di_i2c` module from https://github.com/DexterInd/RFR_Tools that has to be installed and the enabling of the I2C in `raspi-config` menu. 
```
pip install -r requirements.txt
```
```
python3 setup.py install
```

You can also run `python setup.py test` to test import the modules of the GrovePi package that are listed in the [package_modules.txt](package_modules.txt) file. The `python setup.py test` commands should be run after pip installing the dependencies.

## Library Breakdown

There are 2 kind of example scripts:

1. Example programs that only require the `grovepi` module - these example scripts are found in this directory (or root directory of the Python package).

1. Example programs that are based on other sublibraries other than the `grovepi` module - these example scripts are found in the subdirectories of this directory.

The libraries installed with the GrovePi package are listed in [here](package_modules.txt).

## Python Consideration

Even though you can install the GrovePi package for both versions of it (2.x and 3.x), some libraries other than the main one (`grovepi.py`) can only be used with Python3. Therefore, it's just better to use Python 3 by-default, instead of relying on an older version of Python which will anyway get retired in the very near future.

## Equipments Used
List of equipments used:

* [Seeed Studio. “Raspberry Pi 4 Computer Model B 4GB.”](https://www.seeedstudio.com/Raspberry-Pi-4-Computer-Model-B-4GB-p-4077.html "https://www.seeedstudio.com/Raspberry-Pi-4-Computer-Model-B-4GB-p-4077.html").
* [Seeed Studio. “GrovePi+.”](https://www.seeedstudio.com/GrovePi.html "https://www.seeedstudio.com/GrovePi.html").
* [Seeed Studio. “Grove - PIR Motion Sensor.”](https://www.seeedstudio.com/Grove-PIR-Motion-Sensor.html "https://www.seeedstudio.com/Grove-PIR-Motion-Sensor.html").


## Helper Function
```
Helper function -h
usage: PIR motion sensor [-h] [-t [timer]] [-m [mode]]

Configurable motion sensor

optional arguments:
  -h, --help            show this help message and exit
  -t [timer], --timer [timer]
                        Set timer
  -m [mode], --mode [mode]
                        Sensitivity level from [1 - 3]: 1. High 2. Medium 3. Low
```
```
Example:

 python3 grove_pir_motion_sensor_modified.py -s 1
 python3 grove_pir_motion_sensor_modified.py -t 20 -s 1
 
Result:
 -
 -
 Motion Detected Fri Apr 30 18:22:03 2021
 Motion Detected Fri Apr 30 18:22:05 2021
 -
 -
```
