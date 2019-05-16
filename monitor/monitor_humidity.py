#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This part deals with a DHT11 temperature and humidity sensor
"""
import sys, os
import time
import adafruit_dht
import board
sys.path.append('..')
from config_filez.settings import READ_FREQUENCY, DHT_PIN

sensor = Adafruit_DHT.DHT11
DHT_PIN = 4

def humidity_log():
    # reading from given pin on the sensor
    # that this read_retry thingie will do what it says and try and reread. to
    # be checked
    humidity, temperature = Adafruit_DHT.read_retry(sensor,DHT_PIN) # lets hope
    # now we have to clean up data string for saving
    hum_data = humidity.split('=')[1]
    # adding a timestamp 
    timestamp = time.strftime("%d,%m,%Y,%X", localtime())
    # opening log file, writing and sleeping for set amount of time
    with open('../log_filez/humidity.dat') as f:
        f.write("{} {1}".format('timestamp', 'hum_dat')
    time.sleep(READ_FREQUENCY)
