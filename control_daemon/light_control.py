#!/usr/bin/env python
#-*- encoding UTF-8 -*-

'''  here lives part of the code that controls lights
a lot depends on what kind of LED strip we're controling.
Guess we're going to use MOSFET for controling the light strenght - we could
have a fine grained control over the light strenght. Also we could have an
RGB strip but those are more expensive and not really neccessary for a
greenhouse setup. Therefore I'm going to go with plain white LED strip. YMMV.
Another note: it would be perhaps beneficial to employ PID.
'''

import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_WS2801.SPI as SPI
from datetime import datetime, time
import schedule
import board
import busio
import adafruit_tsl2561
# those are for the until_sunrise function
import sys, os
import configparser
from config_filez.light import SUNRISE, SUNSET, REQUIRED_LIGHT, RGB_SHIFT, LIGHT_PIN

sys.path.append('..')

# reading config file
cfg = configparser.ConfigParser()
config_f = ('../settings_config_parser.py')
cfg.read(config_f)
sunrise = cfg.getint('light', 'time_on')
sunset = cfg.getint('light', 'time_off')
light_min = cfg.getint('light', 'light_min')
light_max = cfg.getint('light', 'light_max')
red = cfg.getint('light', 'rgb_red')
green = cfg.getint('light', 'rgb_green')
blue = cfg.geting('light', 'rgb_blue')

#rewrite light function so that it uses PID and configparser!

def light():
    # t2 = 'SUNSET'
    # t1 = 'SUNRISE'
    i2c = busio.I2C(board.SCL, board.SDA)   # create I2C bus
    tsl = adafruit_tsl2561.TSL2561(i2c)     # create TSL2561 instance
    tsl.enabled = True                      # in the I2C bus
    lux = tsl.lux()
    tries = 0
    if not lux == None and tries < 10:
        if lux < REQUIRED_LIGHT:
            GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW) # relay LOW = ON
        else:
            GPIO.setup(LIGHT_PIN, GPIO.OUT, initial=GPIO.HIGH) # turn light off
    else:
        GPIO.setup(LIGHT_PIN, GPIO.OUT, inititial=GPIO.HIGH) # turn light off
        time.sleep(0.2)
        tries += 1
    time.sleep(15)
schedule.every().day.at(SUNSET).do(light())    # fix this it doesn't work

# ad a function pausing it from SUNSET variable
# here it comes:

def until_sunrise(t1=SUNRISE, t2=SUNSET):

    t1_H, t1_M = t1.split(':')
    t2_H, t2_M = t2.split(':')

    t1_int = int(t1_H) * 3600 + int(t1_M) * 60
    t2_int = int(t2_H) * 3600 + int(t2_M) * 60

    t3 = ( 86400 - t2_int + t1_int) # time from sunset untill the next sunrise
                                # in seconds
    return t3


schedule.every().day.at(SUNSET).do(sleep(t3)) # fix this it doesn't work with
        # that SUNSET variable
