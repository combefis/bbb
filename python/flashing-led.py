#!/usr/bin/env python
# flashing-led.py
# author: Sébastien Combéfis
# version: February 28, 2017

import os.path
import time

# Activate GPIO P9_42
if not os.path.exists('/sys/class/gpio/gpio7'):
    with open('/sys/class/gpio/export', 'w') as file:
        file.write('7')

    with open('/sys/class/gpio/gpio7/direction', 'w') as file:
        file.write('out')

# Activate ADC
if not os.path.exists('/sys/devices/bone_capemgr.9/slots'):
    with open('/sys/devices/bone_capemgr.9/slots', 'w') as file:
        file.write('cape-bone-iio')

# Flash the LED
while True:
    value = 1
    with open('/sys/devices/ocp.3/helper.15/AIN0', 'r') as file:
        value = (1799 / int(file.read())) / 100.0
    
    with open('/sys/class/gpio/gpio7/value', 'w') as file:
        file.write('1')    
    time.sleep(value)
    with open('/sys/class/gpio/gpio7/value', 'w') as file:
        file.write('0')
    time.sleep(value)
