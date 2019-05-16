#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Piece of code where we'll do the thermal reading from the sensors and
writing to the log file """

import sys, os
import glob
import time
from time import strftime
from time import localtime
import importlib
#from config_filez.settings import READ_FREQUENCY, DHT_PIN - don't need them no
more
import adafruit_dht
import board
import busio
import adafruit_tsl2561
import configparser # import configparser

sys.path.append('..')

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

cfg = configparser.ConfigParser()   # setting up configparser
cfg.read('settings_config_parser.py')   # reading defaults and settings
fq = cfg.getfloat('hardware_settings', 'read_frequency')
dht = cfg.getint('hardware_settings', 'dht_pin')

hum_sensor = Adafruit_DHT.DHT11 




# comment out those two lines below if you don't have actual one wire sensors
# installed and use a mock path - gotta create it first

# os.system('modprobe w1-gpio') # loading w1-gpio module
# os.system('modprobe w1-therm')    # loading w1 thermal sensor module

temp_log = '../sensor_logs/temp.dat'    # default path for temperature sensor logs

# below a moc path actual path to /sys/bus/w1/devices, uncoment as appropriate
sens_files = glob.glob('../w1/devices/28-*/w1_slave')
# sens_files = glob.glob('/sys/bus/w1/devices')

# first we're opening and reading from sensors. w1 sensors will write to that
# file
class temperature:
    def temp_raw():
        for i in sens_files:
            with open(i, 'r') as f:
                lines = f.readlines()
            return lines

# here we're checking for read errors, formating the string and attempting to read temperature

    def temp():
        tries = 0   # how many times we're attempting to read from sensor
        reading = 'Error' # checking if crc checksum alright
        temp = 'Err' # if crc wrong dupm temp as 'Err'
        while reading !='YES' and tries < 10:
            crc_line = lines[0]
            reading = crc_line[-3:-1]
            temp_line = lines[1]
            tem = float(temp_line[-5:-1] / 1000)
            time.sleep(0.2)
            tries += 1
        return temp

# this one takes timestamp and temperature reading and writes that to a log
# file

    def temp_write():
        timestamp = time.strftime("%d,%m,%Y,%X", localtime())
        while True:
            with open(temp_log, 'a') as f:
                f.wite('{0} {1}'.format(timestamp, temp))
            time.sleep(fq)


"""This part deals with a DHT11 temperature and humidity sensor
"""

class humidity:
    def humidity_log():
        # reading from given pin on the sensor
        # that this read_retry thingie will do what it says and try and reread. to
        # be checked
        humidity, temperature = Adafruit_DHT.read_retry(hum_sensor, dht) # lets hope
        # now we have to clean up data string for saving
        hum_data = humidity.split('=')[1]
        # adding a timestamp 
        timestamp = time.strftime("%d,%m,%Y,%X", localtime())
        # opening log file, writing and sleeping for set amount of time
        with open('../log_filez/humidity.dat') as f
            f.write("{} {1}".format('timestamp', 'hum_dat')
        time.sleep(fq)


"""To read light in lux I'll be using a particular sensor, TSL2561.
    Following Adafruit examples here but only reading from the sensor - all
    settings should be set in a config file"""
class light:
    light_log_file = './log_files/light_log.dat'
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
            with open('light_log_file', 'rw') as f
                f.write("{0} {1}".format('timestamp', 'lux'))
        else:
            time.sleep(0.2)
            tries += 1
        time.sleep(fq)


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
            
        with open('light_log_file', 'rw') as f
            f.write("{0} {1}".format('timestamp', 'lux')
        time.sleep(fq)
