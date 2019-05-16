#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module reads desired temperature from config file and manages PID to get
there. First implementation is aimed at using two relays, one for the heater,
the other for a vent or a servo opening a window.
Author: erg
Date: 14.05.2019
"""
# this one requires us to install simple-pid via 'pip install simple-pid'
# as well as MPC4725 from Adafruit
from simple_pid import PID
import Adafruit_MCP4725
import configparser
import time

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
vent_man = ('temperature', 'bool_venting_manual')
kp = cfg.getfloat('hardware_settings', 'kp')
ki = cfg.getfloat('hardware_settings', 'ki')
kd = cfg.getfloat('hardware_settings', 'd')
fq = cfg.getint('hardware_settings', 'read_frequency')

#getting last reading from the log file and processing it

class AirVent():


    def __init__(self):
        with open(temp_log, 'r') as tmp:
            for last_line in tmp:
                pass
        timestamp, temp1, temp2 = last.split(' ')
        self.av_temp = (temp1 + temp2)/2

    def update(self, vent_signal)
        while vent_signal < 0:
            self.vent_power = -vent_signal
            with open(temp_log, 'r') as tmp:
                for last_line in tmp:
                    pass
            timestamp, temp1, temp2 = last.split(' ')
            self.av_temp = (temp1 + temp2)/2
            self.vent_power = -vent_signal
        return self.vent_power


if __name__ == '__main__':
    vent = AirVent()
    vent_power = vent.vent_power
    #setting up pid
    pid = PID(kp, ki, kd, setpoint=minimux)

#main loop in which pid runs
    if (vent_man = True and trigers_sensors = True):
        pid.automode = True
        pid.sample_time = fq
        pid.setpoint = minimum
        pid.proportional_on_measurement = True
        pid.output_limits = (dac_min, dac_max)
        while True: 
            vent_power = pid(av_temp)
            dac_vent.set_voltage = output
            time.sleep(fq)
    else:
        pid.automode = False
        time.sleep(fq)
