#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""To read light in lux I'll be using a particular sensor, TSL2561.
    Following Adafruit examples here but only reading from the sensor - all
    settings should be set in a config file"""

import sys, os
import board
import busio
import adafruit_tsl2561
import time
sys.path.append('..')
from config_filez.settings import READ_FREQUENCY


log_file = './log_files/light_log.dat'



# create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create TSL2561 instance, passing in the I2C bus
tsl = adafruit_tsl2561.TSL2561(i2c)

# enable sensor
tsl.enabled = True

def light()
    lux = tsl.lux()
    tries = 0
    timestamp = time.strftime("%d,%m,%Y,%X", localtime())
    if lux is not None and tries < 10:
        with open('log_file', 'rw') as f
            f.write("{0} {1}".format('timestamp', 'lux'))
    else:
        time.sleep(0.2)
        tries += 1
    time.sleep(READ_FREQUENCY)


# This is a second take on that function I think perhaps more correct. Is it?

def light1()
    lux = tsl.lux()
    tries = 0
    timestamp = time.strftime("%d,%m,%Y,%X", localtime())
    if lux is None and tries < 10:
        time.sleep(0.2)
        tries += 1
        continue
    elif lux is None and tries == 10:
        lux = "Err"
    else lux is not None and tries < 10:
        return lux
        
    with open('log_file', 'rw') as f
        f.write("{0} {1}".format('timestamp', 'lux')
    time.sleep(READ_FREQUENCY)
