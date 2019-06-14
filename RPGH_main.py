#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
This is the main program starting the GUI, monitor and control deamons (TBI).

Things to implement:
- connect all the buttons
- decide how to display graphs and write that (battery level?)
- continue developing the control daemon
- write up alerts and conditions for them
- figure out how to manage buttons in groupBoxes
- figure out how to get data of the checkBoxes and radioButtons
- in mplwidget histogram doesn't do what I want it to: figure out how to plot
  data against y_axis with datetime data
- write function to get battery levels
- write function to get data of the rain gauge
- write function to get data of the soil moisture sensors

Author: uinarf
Date: 21.05.2019
"""

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick, uic
import matplotlib
matplotlib.use('qt5agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import dates
import numpy as np
from datetime import datetime
import configparser
from RPGH_main_gui import Ui_MainWindow

# code from module below doesn't work unles on Pi, uncoment and test once there
# from monitor_unified import Light.light_read

sys.path.append('..')

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

# read and extract/format configuration data
config_f = 'settings_config_parser.py'
cfg = configparser.ConfigParser()
cfg.read('settings_config_parser.py')

# Data used to be extracted explicitly like that which was somewhat more clear,
# management decided against it...
# light management data
#light_min = cfg.getint('light', 'light_min')
#light_max = cfg.getint('light', 'light_max')
#light_time_on_to_convert = cfg.get('light', 'time_on')
#light_time_on = datetime.strptime(light_time_on_to_convert, '%H:%M').time()


# those below are for displaying current light measurement, won't
# work without monitor_unified AND RPi:
# light_current_visible = light_read().[1]
# light_current_broadband = light_read().[2]
# light_current_infrared = light_read().[3]

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):

        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        #self.ui = uic.loadUi(LOCAL_DIR + "Tab_Widget_main_GUI_03.ui", self)

# light management tab
# missing groupBox with sensor/time/off choice
        self.light_light_min.setValue(cfg.getint('light', 'light_min'))
        self.light_light_min.valueChanged.connect(self.write_light_min)

        self.light_light_max.setValue(cfg.getint('light', 'light_max'))
        self.light_light_max.valueChanged.connect(self.write_light_max)

        self.light_rgb_red.setValue(cfg.getint('light', 'rgb_red'))
        self.light_rgb_red.valueChanged.connect(self.write_light_rgb_red)

        self.light_rgb_green.setValue(cfg.getint('light', 'rgb_green'))
        self.light_rgb_green.valueChanged.connect(self.write_light_rgb_green)

        self.light_rgb_blue.setValue(cfg.getint('light', 'rgb_blue'))
        self.light_rgb_blue.valueChanged.connect(self.write_light_rgb_green)

#        self.light_sensor_lcd_visible.display(light_current_visible)

#        self.light_sensor_lcd_broadband.display(light_current_broadband)

#        self.light_sensor_lcd_infrared.display(light_current_infrared)

# changed GUI, don't need those no more
#        self.light_bool_normalise.setChecked(cfg.getboolean('light',
#        'bool_normalise'))
#        self.light_bool_normalise.clicked.connect(self.write_light_normalise)

        self.light_bool_alert.setChecked(cfg.getboolean('light', 'bool_alert'))
#        self.light_bool_alert.clicked.connect(self.write_light_alert)
# Those comented lines do not work. Check the sender?
#       self.light_bool_alert.isChecked(self.write_light_normalise)

        self.light_time_on.setTime(datetime.strptime(cfg.get('light',
        'light_time_on'), '%H:%M').time())
        self.light_time_on.timeChanged.connect(self.write_light_time_on)

        self.light_time_off.setTime(datetime.strptime(cfg.get('light',
        'light_time_off'), '%H:%M').time())
        self.light_time_off.timeChanged.connect(self.write_light_time_off)

# temperature management tab
# missing groupBox with sensor/time/off choice
        self.temperature_temp_min.setValue(cfg.getint('temperature', 'temp_min'))
        self.temperature_temp_min.valueChanged.connect(self.write_temp_min)

        self.temperature_temp_max.setValue(cfg.getint('temperature',
        'temp_max'))
        self.temperature_temp_max.valueChanged.connect(self.write_temp_max)

        self.temperature_time_heating_on.setTime(datetime.strptime(cfg.get('temperature',
        'time_heating_on'), '%H:%M').time())
        self.temperature_time_heating_on.timeChanged.connect(self.write_temp_heating_time_on)

        self.temperature_time_heating_off.setTime(datetime.strptime(cfg.get('temperature',
        'time_heating_off'), '%H:%M').time())
        self.temperature_time_heating_off.timeChanged.connect(self.write_temp_heating_time_off)

        self.temperature_time_venting_on.setTime(datetime.strptime(cfg.get('temperature',
        'time_venting_on'), '%H:%M').time())
        self.temperature_time_venting_on.timeChanged.connect(self.write_temp_vent_time_on)

        self.temperature_time_venting_off.setTime(datetime.strptime(cfg.get('temperature',
        'time_venting_off'), '%H:%M').time())
        self.temperature_time_venting_off.timeChanged.connect(self.write_temp_vent_time_off)

# humidity management tab
# missing groupBox with sensor/off choice
        self.humidity_humidity_min.setValue(cfg.getint('humidity', 'humidity_min'))
        self.humidity_humidity_min.valueChanged.connect(self.write_hum_min)

        self.humidity_humidity_max.setValue(cfg.getint('humidity', 'humidity_max'))
        self.humidity_humidity_max.valueChanged.connect(self.write_hum_max)

# water management tab
        self.water_soil_moisture_min.setValue(cfg.getint('water', 'soil_moisture_min'))
        self.water_soil_moisture_min.valueChanged.connect(self.write_soil_moisture_min)

        self.water_soil_moisture_max.setValue(cfg.getint('water', 'soil_moisture_max'))
        self.water_soil_moisture_max.valueChanged.connect(self.write_soil_moisture_max)

        self.water_time_of_watering.setTime(datetime.strptime(cfg.get('water',
        'time_of_watering'), '%H:%M').time())
#        self.water_time_of_watering.valueChanged.connect()

        self.water_time_watering_duration.setTime(datetime.strptime(cfg.get('water',
        'time_watering_duration'), '%H:%M').time())
#        self.water_time_watering_duration.valueChanged.connect()

        self.water_amount.setValue(cfg.getint('water', 'amount'))
#        self.water_amount.valueChanged.connect()

# alerts tab

        self.alerts_bool_on_screen.setChecked(cfg.getboolean('alerts',
        'bool_on_screen'))
        self.alerts_text_on_screen.setText(cfg.get('alerts', 'text_on_screen'))

        self.alerts_bool_sound.setChecked(cfg.getboolean('alerts',
        'bool_sound'))
        self.alerts_path_sound.setText(cfg.get('alerts', 'path_sound'))

        self.alerts_bool_sms.setChecked(cfg.getboolean('alerts', 'bool_sms'))
        self.alerts_sms_number.setText(cfg.get('alerts', 'sms_number'))

        self.alerts_bool_email.setChecked(cfg.getboolean('alerts',
        'bool_email'))
        self.alerts_email_address.setText(cfg.get('alerts', 'email_address'))
# manual tab

        self.manual_bool_light_on.setChecked(cfg.getboolean('manual',
        'bool_light_on'))
        self.manual_bool_light_off.setChecked(cfg.getboolean('manual',
        'bool_light_off'))

        self.manual_bool_water_on.setChecked(cfg.getboolean('manual',
        'bool_water_on'))
        self.manual_bool_water_off.setChecked(cfg.getboolean('manual',
        'bool_water_off'))

        self.manual_bool_heating_on.setChecked(cfg.getboolean('manual',
        'bool_heating_on'))
        self.manual_bool_heating_off.setChecked(cfg.getboolean('manual',
        'bool_heating_off'))

        self.manual_bool_vent_on.setChecked(cfg.getboolean('manual',
        'bool_vent_on'))
        self.manual_bool_vent_off.setChecked(cfg.getboolean('manual',
        'bool_vent_off'))

# setting up mplwidget
        self.mplwidget()


    def mplwidget(self):

        temp_log = 'sensor_logs/temperature_out.dat'
#        temp_log = 'sensor_logs/temperature_out.dat'
        time_format = '%d,%m,%Y,%X'
        timestamp = []
        temp_up = []
        temp_down = []
        temp_ground = []

        with open(temp_log, 'r') as temperature:
            for i, line in enumerate(temperature):
                a, b, c, d = line.split(' ')
                timestamp.append(datetime.strptime(a, time_format))
                temp_up.append(float(b))
                temp_down.append(float(c))
                temp_ground.append(float(d))

        time_format = '%d,%m,%Y,%X'
        light_log = 'sensor_logs/light_data.dat'
        timestamp_1 = []
        visible = []
        broadband = []
        infrared = []
        with open(light_log, 'r') as light:
            for j, lines in enumerate(light):
                d, e, n, m = lines.split(' ')
                timestamp_1.append(datetime.strptime(d, time_format))
                visible.append(int(e))
                broadband.append(int(n))
                infrared.append(int(m))

        time_format = '%d,%m,%Y,%X'
        hum_log = 'sensor_logs/hum_data_ordered.dat'
        timestamp_2 = []
        humid = []
        with open(hum_log, 'r') as humidity:
            for i, lines in enumerate(humidity):
                a, b = lines.split(' ')
                timestamp_2.append(datetime.strptime(a, time_format))
                humid.append(float(b))

        moist_log = 'sensor_logs/soil_hum.dat'
        timestamp_3 = []
        moist = []
        with open(moist_log, 'r') as moisture:
            for i, lines in enumerate(moisture):
                a, b = lines.split(' ')
                timestamp_3.append(datetime.strptime(a, time_format))
                moist.append(float(b))

# this section is ready to be deployed in case there's an issue with displaying
# datetime data. May have to specify datemin as something like but at the
# moment that would mess with mock data
#        datemin = datetime.now() - timedelta(hours=24)
#        datemax = datetime.now()
# datemin/max below were dummy in sync with .dat file timestamps
#        datemin = datetime(2019, 3, 22, 13, 0, 3)
#        datemax = datetime(2019, 3, 22, 13, 10, 4)

#        days = dates.DayLocator()
#        hours = dates.HourLocator()
#        minutes = dates.MinuteLocator()
#        seconds = dates.SecondLocator()
#        dfmt = dates.DateFormatter('%b %d')
#        tmfd = dates.DateFormatter('%H %M')
# setting up how we display data
#        self.mpl.canvas.ax.xaxis.set_major_locator(hours)
#        self.mpl.canvas.ax.xaxis.set_major_formatter(dfmt)
#        self.mpl.canvas.ax.xaxis.set_minor_locator(minutes)
#        self.mpl.canvas.ax.xaxis.set_minor_formatter(tmfd)
#        self.mpl.canvas.ax.set_xlim(datemin, datemax)
#        self.fig = Figure()
#        self.ax = self.fig.add_subplot(311)
#        self.ax_1 = self.fig.add_subplot(312)
#        self.ax_2 = self.fig.add_subplot(313)
        self.mpl.canvas.ax.set_ylabel('Temperature C')
        self.mpl.canvas.ax.grid(True)
# ploting temperature data
        self.mpl.canvas.ax.plot(timestamp, temp_up, c='red', ls=':',
        label='temp_up')
        self.mpl.canvas.ax.plot(timestamp, temp_down, c='orange', ls='dotted',
        label='temp_down')
        self.mpl.canvas.ax.plot(timestamp, temp_ground, c='brown', ls='-',
        label='ground temperature')
        self.mpl.canvas.ax.fill_between(timestamp, temp_up, temp_down)
        self.mpl.canvas.ax.legend()
# adding light subplot
        self.mpl.canvas.ax_1.set_ylabel('Light lm')
        self.mpl.canvas.ax_1.grid(True)
        self.mpl.canvas.ax_1.plot(timestamp_1, visible, c='cyan', ls='-.',
        label='broadband')
        self.mpl.canvas.ax_1.plot(timestamp_1, broadband, c='orange', ls='-.',
        label='visible')
        self.mpl.canvas.ax_1.plot(timestamp_1, infrared, c='red', ls='-.',
        label='infrared')
        self.mpl.canvas.ax_1.legend()
# adding humidity subplot
        self.mpl.canvas.ax_2.set_ylabel('Humidity/watering %')
        self.mpl.canvas.ax_2.grid(True)
        self.mpl.canvas.ax_2.plot(timestamp_2, humid, c='blue', ls='--',
        label='humidity')
# adding to it soil humidity data
        self.mpl.canvas.ax_2.plot(timestamp_3, moist, c='navy', ls=' ',
        label='soil_moisture')
        self.mpl.canvas.ax_2.fill_between(timestamp_2, 0, moist)
        self.mpl.canvas.ax_2.legend()
# decorating
# interestingly, line below seems not neccessary
#        self.mpl.canvas.draw()

# setting up weather station tab:
# adding temperature plot
        self.mpl1.canvas.ax.set_ylabel('Temperature C')
        self.mpl1.canvas.ax.grid(True)
        self.mpl1.canvas.ax.plot(timestamp, temp_up, c='orange', ls='-.',
        label='temperature outdoors')
# adding light plot
        self.mpl1.canvas.ax_1.set_ylabel('Light lm')
        self.mpl1.canvas.ax_1.grid(True)
        self.mpl1.canvas.ax_1.plot(timestamp_1, visible)
# adding humidity/rainfall graph
# mind you that hist() doesn't do what I'd like it to do. redo.
        self.mpl1.canvas.ax_2.set_ylabel('Humidity/rainfall %')
        self.mpl1.canvas.ax_2.grid(True)
        self.mpl1.canvas.ax_2.hist(humid, bins=24)

# defining light management ui write actions (could be rewriten, lots of
# redundant code

    def write_light_min(self):
        send = self.light_light_min.value()
        message = str(send)
        cfg.set('light', 'light_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)
        return

    def write_light_max(self):
        send = self.light_light_max.value()
        message = str(send)
        cfg.set('light', 'light_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_light_rgb_red(self):
        send = self.light_rgb_red.value()
        message = str(send)
        cfg.set('light', 'light_rgb_red', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_light_rgb_green(self):
        send = self.light_rgb_green.value()
        message = str(send)
        cfg.set('light', 'light_rgb_green', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_light_rgb_blue(self):
        send = self.light_rgb_blue.value()
        message = str(send)
        cfg.set('light', 'light_rgb_blue', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

# Those QCheckBoxes do not seem to have a .value() property - what then?
# changed GUI, don't need those no more
#    def write_light_normalise(self):
#        send = self.light_bool_normalise.value()
#        message = str(send)
#        cfg.set('light', 'light_normalise', message)
#        with open(config_f, 'w') as conffile:
#            cfg.write(conffile)

#    def write_light_alert(self):
#        send = self.light_bool_alert.value()
#        message = str(send)
#        cfg.set('light', 'light_alert', message)
#        with open(config_f, 'w') as conffile:
#            cfg.write(conffile)

    def write_light_time_on(self):
        send = self.light_time_on.time()
        message = send.toString(self.light_time_on.displayFormat())
        cfg.set('light', 'light_time_on', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_light_time_off(self):
        send = self.light_time_off.time()
        message = send.toString(self.light_time_off.displayFormat())
        cfg.set('light', 'light_time_off', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

# defining temperature management tab

    def write_temp_min(self):
        send = self.temperature_temp_min.value()
        message = str(send)
        cfg.set('temperature', 'temp_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_temp_max(self):
        send = self.temperature_temp_max.value()
        message = str(send)
        cfg.set('temperature', 'temp_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_temp_heating_time_on(self):
        send = self.temperature_time_heating_on.time()
        message = send.toString(self.temperature_time_heating_on.displayFormat())
        cfg.set('temperature', 'temp_heating_on', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_temp_heating_time_off(self):
        send = self.temperature_time_heating_off.time()
        message = send.toString(self.temperature_time_heating_off.displayFormat())
        cfg.set('temperature', 'temp_heating_off', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_temp_vent_time_on(self):
        send = self.temperature_time_venting_on.time()
        message = send.toString(self.temperature_time_venting_on.displayFormat())
        cfg.set('temperature', 'temp_vent_on', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_temp_vent_time_off(self):
        send = self.temperature_time_venting_off.time()
        message = send.toString(self.temperature_time_venting_off.displayFormat())
        cfg.set('temperature', 'temp_vent_on', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

# defining humidity management tab
    def write_hum_min(self):
        send = self.hum_min.value()
        message = str(send)
        cfg.set('humidity', 'humidity_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_hum_max(self):
        send = self.hum_max.value()
        message = str(send)
        cfg.set('humidity', 'humidity_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

# defining water management tab
    def write_soil_moisture_min(self):
        send = self.soil_moisture_min.value()
        message = str(send)
        cfg.set('water', 'soil_moisture_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_soil_moisture_max(self):
        send = self.soil_moisture_max.value()
        message = str(send)
        cfg.set('water', 'soil_moisture_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)
# defining hardware settings management tab
    def write_fq(self):
        send = self.hardware_settings_read_frequency.value()
        message = str(send)
        cfg.set('hardware_settings', 'read_frequency', message)
        with open('settings_config_parser.py', 'w') as conffile:
            cfg.write(conffile)
        return

if __name__ == '__main__':
    app = QtWidgets.QApplication([sys.argv])
    gui = DesignerMainWindow()
    gui.show()
    sys.exit(app.exec_())
