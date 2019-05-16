#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Piece of code where we'll do the thermal reading from the sensors and
writing to the log file """

import sys
import os
import glob
import time
from time import strftime
from time import localtime
import importlib
sys.path.append('..')
from config_filez.settings import READ_FREQUENCY

    # comment out those two lines below if you don't have actual one wire sensors
    # installed and use a mock path - gotta create it first

# os.system('modprobe w1-gpio') # loading w1-gpio module
# os.system('modprobe w1-therm')    # loading w1 thermal sensor module

temp_log = '../sensor_logs/temp.dat'    # default path for sensor logs

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
            time.sleep(READ_FREQUENCY)
