#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module reads desired temperature from config file and manages PID to get
there. First implementation is aimed at using two relays, one for the heater,
the other for a vent or a servo opening a window.
Author: uinarf
Date: 14.05.2019
"""
# this one requires us to install simple-pid via 'pip install simple-pid'
# as well as MPC4725 from Adafruit
from simple_pid import PID
import Adafruit_MCP4725
import configparser
import time
import sys, os
import glob
# setting up DAC. Output is range 0-4096
dac_vent = Adafruit_MCP4725()
dac_min = 0
dac_max = 4096

# here log/setting files
temp_log = 'temperature_out.dat'
config_f = 'settings_config_parser.py'
cfg = configparser.ConfigParser()
cfg.read(config_f)
#maximum = cfg.getint('temperature', 'temp_max')
minimum = cfg.getint('temperature', 'temp_min')
sens_trig = cfg.get('temperature', 'trigers_sensors ')
#heat_man = ('temperature', 'bool_heating_manual')
vent_man = cfg.getboolean('temperature', 'bool_venting_manual')
kp = cfg.getfloat('temperature', 'kp')
ki = cfg.getfloat('temperature', 'ki')
kd = cfg.getfloat('temperature', 'd')
fq = cfg.getint('hardware_settings', 'read_frequency')

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sens_files = glob.glob('/sys/bus/devices/28-*/w1_slave')

# I've settled for reading from sensors rather than from log files, for better
# or worse.

# I don't really understand what the hell is going on below, I'm going to
# rewrite it, first reading the temperature, then checking the conditions to
# turn vent on and if they're satisfied then creating PID and turning on power
# with PWM

class AirVent_01():

    def temp():
        for i in sens_files:
            with open(i, 'r') as f:
# I reckon I've to substitute 'lines' with 'lines[]' below so as to be able to
# read multiple sensors and not loose those readings
                lines = f.readlines()
            return lines
        tries = 0
# checking if crc checksum's alright if not we're returning temp as evil
# temperature
        reading = 'Error'
        temp = '666'
        while reading != 'YES' and tries < 10:
            crc_line = lines[0]
            reading = crc_line[-3:-1]
            temp_line = lines[1]
            temp = float(temp_line[-5:-1] / 1000)
            time.sleep(0.2)
            tries += 1
        return temp




#class AirVent():
#
#    def __init__(self):
#        with open(temp_log, 'r') as tmp:
#            for last_line in tmp:
#                pass
#        timestamp, temp1, temp2 = last.split(' ')
#        self.av_temp = (temp1 + temp2)/2
#
    def update(self, vent_signal)
        while vent_signal < 0:
# this is for ventilation, guess we'll need to use inverted value
            self.vent_power = -vent_signal
            with open(temp_log, 'r') as tmp:
                for last_line in tmp:
                    pass
            timestamp, temp1, temp2 = last.split(' ')
            self.av_temp = (temp1 + temp2)/2
        return self.vent_power


if __name__ == '__main__':
    vent = AirVent()
    vent_power = vent.vent_power
    #setting up pid
    pid = PID(kp, ki, kd, setpoint=minimux)

#main loop in which pid runs
    if (vent_man = True and sens_trig = True):
        pid.automode = True
        pid.sample_time = fq
        pid.setpoint = minimum
        pid.proportional_on_measurement = True
        pid.output_limits = (dac_min, dac_max)
        while True:
            vent_power = pid(av_temp)
            dac_vent.set_voltage = vent_power
            time.sleep(fq)
    else:
        pid.automode = False
        time.sleep(fq)
