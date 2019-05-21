#!/usr/bin/env python
#-*- encoding UTF-8 -*-

'''Light controls. Read from settings and sensor, check time, set up PID and
PWM. Needs to be amended in the future if we're to control RGB of the LED's as
well. Using PWM for light control insead of DAC.
Author: uinarf 
Date: 18.05.2019
'''
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_WS2801.SPI as SPI
import time
import schedule
import board
import busio
import adafruit_tsl2561
import sys
import configparser
from simple_pid import PID

sys.path.append('..')

# reading config file
cfg = configparser.ConfigParser()
config_f = ('../settings_config_parser.py')
cfg.read(config_f)
sunrise = cfg.getint('light', 'time_on')
sunset = cfg.getint('light', 'time_off')
light_min = cfg.getint('light', 'light_min')
light_max = cfg.getint('light', 'light_max')
light_man = cfg.getboolean('light', 'bool_manual')
sens_trig = cfg.getboolean('light', 'trigers_sensors')
fq = cfg.getint('hardware_settings', 'read_frequency')
lp_pin = cfg.getint('hardware_settings', 'lp_pin')
#red = cfg.getint('light', 'rgb_red')
#green = cfg.getint('light', 'rgb_green')
#blue = cfg.geting('light', 'rgb_blue')
light_frequency = 100


def light():
    now = time.time()
    while sunrise <= now <= sunset:
        if (light_man = True and sens_trig = True):
# turning on light sensor and getting it's value
            i2c = busio.I2C(board.SCL, board.SDA)   # create I2C bus
            tsl = adafruit_tsl2561.TSL2561(i2c)     # create TSL2561 instance
            tsl.enabled = True                      # in the I2C bus
            lux = tsl.lux()
# creating PID instance and turning it on
            pid = PID(kp, ki, kd, setpoint=light_min)
            pid.automode = True
            pid.sample_time = fq
            pid.setpoint = light_min
            pid.proportional_on_measurement = True
# defining output limits, for PWM that should be 0-100% I guess
            pid.output_limits = (0, 100)
            led_power = pid(lux)
# setting up GPIO
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(lp_pin, GPIO.OUT)
            light_pwm = GPIO.PWM(lp_pin, light_frequency)
            light_pwm.start(led_power)
            while True:
                led_power = pid(lux)
                light_pwm.ChangeDutyCycle(led_power)
                time.sleep(fq)

        else:
            pid.automode = False
            time.sleep(fq)
