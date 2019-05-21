#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Piece of code where we'll do the thermal reading from the sensors and
writing to the log files. Perhaps it would be better to write to a database?
Author: uinarf
Date: 21.05.2019
"""

import sys, os
import glob
import time
from time import strftime
from time import localtime
import importlib
import adafruit_dht
import board
import busio
import adafruit_tsl2561
import configparser

sys.path.append('..')

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

# setting up configparser
cfg = configparser.ConfigParser()
# reading defaults and settings
cfg.read('settings_config_parser.py')
fq = cfg.getint('hardware_settings', 'read_frequency')
dht = cfg.getint('hardware_settings', 'dht_pin')

hum_sensor = Adafruit_DHT.DHT11

# comment out those two lines below if you don't have actual one wire sensors
# installed and use a mock path - gotta create it first

 # loading w1-gpio module
 os.system('modprobe w1-gpio')
 # loading w1 thermal sensor module
 os.system('modprobe w1-therm')


# default path for temperature sensor logs

temp_log = '../sensor_logs/temp.dat'    # default path for temperature sensor logs
light_log = '../sensor_logs/light.dat'
humidity_log = '../sensor_logs/humidity.dat'

# below a moc path and actual path, un/comment as appropriate
sens_files = glob.glob('../w1/devices/28-*/w1_slave')
# sens_files = glob.glob('/sys/bus/w1/devices')

"""
Dealing with 1 wire temperature sensors.
"""

class Temperature:

    def temp():

        temp_list = []
        for i in sens_files:
            with open(i, 'r') as f:
                tries = 0
                reading = 'Error'
# checking if crc checksum ok. if not temp is '-666', NaN
                temp = '-666'
                while reading !='YES' and tries < 10:
                    line = f.readline()
                    reading = line[-4:-1]
                    line = f.readline()
                    temp = float(line[-6:-1]) / 1000
                    time.sleep(0.2)
                    tries += 1
                    temp_list.append(temp)
        return temp_list


    def temp_write():

        timestamp = time.strftime("%d,%m,%Y,%X", localtime())
        while True:
            with open(temp_log, 'a') as f:
                temp_str = ' '.join(str(i) for i in temp_list)
                f.write('{0} {1}'.format(timestamp, temp_str))
            time.sleep(fq)

"""
This part deals with a DHT11 temperature and humidity sensor
"""

class Humidity:
    def humidity():

# To be checked: if this 'read_retry' function does what's on the label. What
# about errors?
        humidity, temperature = Adafruit_DHT.read_retry(hum_sensor, dht)
        hum_data = humidity.split('=')[1]
        return hum_data


    def humidity_write():

        timestamp = time.strftime("%d,%m,%Y,%X", localtime())

        with open(humidity_log, 'a') as f:
            f.write("{} {1}".format('timestamp', 'hum_dat'))
        time.sleep(fq)
"""
This part deals with tsl2561 sensor.
"""

class Light:


    def light_read():

        i2c = busio.I2C(board.SCL, board.SDA)
        tsl = adafruit_tsl2561.TSL2561(i2c)
        tsl.enabled = True
        lux = tsl.lux()
        tries = 0
        timestamp = time.strftime("%d,%m,%Y,%X", localtime())
        if lux is None and tries < 10:
            time.sleep(0.2)
            tries += 1
        elif lux is None and tries == 10:
# report lux as a special NaN on read error
            lux = "-666"
        else:
            lux is not None and tries < 10
        return lux

    def light_write():
        with open(light_log, 'a') as f:
            f.write("{0} {1}".format('timestamp', 'lux'))
        time.sleep(fq)


class Soil_Moisture:
    pass


class Precipitation:
    pass
