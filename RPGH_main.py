#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
This is the main program starting the GUI, monitor and control deamons (TBI).

Things to implement:
- connect all the buttons
- decide how to display graphs and write that (battery level?)
- continue developing the control daemon
- write up alerts and conditions for them
- in mplwidget histogram doesn't do what I want it to: figure out how to plot
  data against y_axis with datetime data
- write function to get battery levels
- write function to get data of the rain gauge
- write function to get data of the soil moisture sensors

Author: uinarf
Date: 21.05.2019
"""

import sys, os
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick, uic
#from PyQt5.QtGui import QKeySequence
#from PyQt5.QtWidgets import QShortcut, QAction
import matplotlib
matplotlib.use('qt5agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import dates
import numpy as np
from datetime import datetime
import configparser
from RPGH_main_gui import Ui_MainWindow
from PID_warning import Ui_Dialog
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from PyQt5.QtWidgets import QDialog

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
        self.light_trigers_off.setChecked(cfg.getboolean('light',
        'trigers_off'))
        self.light_trigers_off.clicked.connect(self.write_light_trigers)

        self.light_trigers_time.setChecked(cfg.getboolean('light',
        'trigers_clock'))
        self.light_trigers_time.clicked.connect(self.write_light_trigers)

        self.light_trigers_sensors.setChecked(cfg.getboolean('light',
        'trigers_sensors'))
        self.light_trigers_sensors.clicked.connect(self.write_light_trigers)

        self.light_light_min.setValue(cfg.getint('light', 'light_min'))
        self.light_light_min.valueChanged.connect(self.write_light_min)
        self.light_light_min.valueChanged.connect(self.mpl_replot)

        self.light_light_max.setValue(cfg.getint('light', 'light_max'))
        self.light_light_max.valueChanged.connect(self.write_light_max)
        self.light_light_max.valueChanged.connect(self.mpl_replot)

        self.light_rgb_red.setValue(cfg.getint('light', 'rgb_red'))
        self.light_rgb_red.valueChanged.connect(self.write_light_rgb_red)
        self.light_rgb_red.valueChanged.connect(self.mpl_replot)

        self.light_rgb_green.setValue(cfg.getint('light', 'rgb_green'))
        self.light_rgb_green.valueChanged.connect(self.write_light_rgb_green)
        self.light_rgb_green.valueChanged.connect(self.mpl_replot)

        self.light_rgb_blue.setValue(cfg.getint('light', 'rgb_blue'))
        self.light_rgb_blue.valueChanged.connect(self.write_light_rgb_green)
        self.light_rgb_blue.valueChanged.connect(self.mpl_replot)

        self.light_control_onoff.setChecked(cfg.getboolean('light',
        'control_onof'))
        self.light_control_onoff.clicked.connect(self.write_control)

        self.light_control_pid.setChecked(cfg.getboolean('light',
        'control_pid'))
        self.light_control_pid.clicked.connect(self.write_control)
        self.light_control_pid.clicked.connect(self.ui_dialog)

        self.light_pid_control_kp.setValue(cfg.getfloat('light', 'kp'))
        self.light_pid_control_kp.valueChanged.connect(self.write_light_kp)

#        self.light_sensor_lcd_visible.display(light_current_visible)

#        self.light_sensor_lcd_broadband.display(light_current_broadband)

#        self.light_sensor_lcd_infrared.display(light_current_infrared)

        self.light_bool_alert.setChecked(cfg.getboolean('light', 'bool_alert'))
        self.light_bool_alert.stateChanged.connect(self.write_light_alert)

        self.light_time_on.setTime(datetime.strptime(cfg.get('light',
        'light_time_on'), '%H:%M').time())
        self.light_time_on.timeChanged.connect(self.write_light_time_on)

        self.light_time_off.setTime(datetime.strptime(cfg.get('light',
        'light_time_off'), '%H:%M').time())
        self.light_time_off.timeChanged.connect(self.write_light_time_off)


# temperature management tab
        self.temperature_trigers_off.setChecked(cfg.getboolean('temperature',
        'trigers_off'))
        self.temperature_trigers_off.clicked.connect(self.write_temperature_trigers)

        self.temperature_trigers_time.setChecked(cfg.getboolean('temperature',
        'trigers_clock'))
        self.temperature_trigers_time.clicked.connect(self.write_temperature_trigers)

        self.temperature_trigers_sensors.setChecked(cfg.getboolean('temperature',
        'trigers_sensors'))
        self.temperature_trigers_sensors.clicked.connect(self.write_temperature_trigers)

        self.temperature_temp_min.setValue(cfg.getint('temperature', 'temp_min'))
        self.temperature_temp_min.valueChanged.connect(self.write_temp_min)
        self.temperature_temp_min.valueChanged.connect(self.mpl_replot)

        self.temperature_temp_max.setValue(cfg.getint('temperature',
        'temp_max'))
        self.temperature_temp_max.valueChanged.connect(self.write_temp_max)
        self.temperature_temp_max.valueChanged.connect(self.mpl_replot)

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

        self.temperature_bool_temp_alert.setChecked(cfg.getboolean('temperature',
        'bool_alert'))
        self.temperature_bool_temp_alert.stateChanged.connect(self.write_temp_alert)

        self.temperature_control_pid.clicked.connect(self.ui_dialog)
# humidity management tab
# missing groupBox with sensor/off choice
        self.humidity_trigers_off.setChecked(cfg.getboolean('humidity',
        'trigers_off'))
        self.humidity_trigers_off.clicked.connect(self.write_humidity_trigers)

        self.humidity_trigers_sensors.setChecked(cfg.getboolean('humidity',
        'trigers_sensors'))
        self.humidity_trigers_sensors.clicked.connect(self.write_humidity_trigers)

        self.humidity_humidity_min.setValue(cfg.getint('humidity', 'humidity_min'))
        self.humidity_humidity_min.valueChanged.connect(self.write_hum_min)
        self.humidity_humidity_min.valueChanged.connect(self.mpl_replot)

        self.humidity_humidity_max.setValue(cfg.getint('humidity', 'humidity_max'))
        self.humidity_humidity_max.valueChanged.connect(self.write_hum_max)
        self.humidity_humidity_max.valueChanged.connect(self.mpl_replot)

        self.humidity_bool_alert.setChecked(cfg.getboolean('humidity',
        'bool_alert'))
        self.humidity_bool_alert.stateChanged.connect(self.write_humidity_bool_alert)

# water management tab
        self.water_trigers_off.setChecked(cfg.getboolean('water',
        'trigers_off'))
        self.water_trigers_off.clicked.connect(self.write_water_trigers)

        self.water_trigers_time.setChecked(cfg.getboolean('water',
        'trigers_clock'))
        self.water_trigers_time.clicked.connect(self.write_water_trigers)

        self.water_trigers_sensors.setChecked(cfg.getboolean('water',
        'trigers_sensors'))
        self.water_trigers_sensors.clicked.connect(self.write_water_trigers)

        self.water_soil_moisture_min.setValue(cfg.getint('water', 'soil_moisture_min'))
        self.water_soil_moisture_min.valueChanged.connect(self.write_soil_moisture_min)
        self.water_soil_moisture_min.valueChanged.connect(self.mpl_replot)

        self.water_soil_moisture_max.setValue(cfg.getint('water', 'soil_moisture_max'))
        self.water_soil_moisture_max.valueChanged.connect(self.write_soil_moisture_max)
        self.water_soil_moisture_max.valueChanged.connect(self.mpl_replot)

        self.water_time_of_watering.setTime(datetime.strptime(cfg.get('water',
        'time_of_watering'), '%H:%M').time())
        self.water_time_of_watering.timeChanged.connect(self.write_watering_time)

        self.water_time_watering_duration.setTime(datetime.strptime(cfg.get('water',
        'time_watering_duration'), '%H:%M').time())
        self.water_time_watering_duration.timeChanged.connect(self.write_watering_duration)

        self.water_amount.setValue(cfg.getint('water', 'amount'))
        self.water_amount.valueChanged.connect(self.write_watering_amount)

        self.water_bool_alert.setChecked(cfg.getboolean('water', 'bool_alert'))
        self.water_bool_alert.stateChanged.connect(self.write_water_bool_alert)

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

# defining log files
        temp_log = 'sensor_logs/temperature_out.dat'
        light_log = 'sensor_logs/light_data.dat'
        hum_log = 'sensor_logs/hum_data_ordered.dat'
        moist_log = 'sensor_logs/soil_hum.dat'

# defining time format
        time_format = '%d,%m,%Y,%X'
# unpacking data settings
        temp_max = cfg.getint('temperature', 'temp_max')
        temp_min = cfg.getint('temperature', 'temp_min')
        light_max = cfg.getint('light', 'light_max')
        light_min = cfg.getint('light', 'light_min')
        humid_max = cfg.getint('humidity', 'humidity_max')
        humid_min = cfg.getint('humidity', 'humidity_min')
        soil_max = cfg.getint('water', 'soil_moisture_max')
        soil_min = cfg.getint('water', 'soil_moisture_min')

# unpacking temperature data
# two styles of reading data, leave 'em here for future reference
        temp_data = pd.read_csv(temp_log, header=None, delim_whitespace=True)
        temp_data.columns = ['timestamp', 'temp_up', 'temp_down', 'temp_ground']
        timestamp_temp = pd.to_datetime(pd.Series(temp_data.timestamp),
        format=time_format)
#        temp_up = temp_data['1']
#        temp_down = temp_data['2']
#        temp_ground = temp_data['3']

# unpacking light data
        light_data = pd.read_csv(light_log, header=None, delim_whitespace=True)
        light_data.columns = ['0','1','2','3']
        timestamp_1 = pd.to_datetime(pd.Series(light_data['0']), format=time_format)
        broadband = light_data['1']
        visible = light_data['2']
        infrared = light_data['3']

# unpacking humidity data
        hum_data = pd.read_csv(hum_log, header=None, delim_whitespace=True)
        hum_data.columns = ['0', '1']
        timestamp_2 = pd.to_datetime(pd.Series(hum_data['0']),
        format=time_format)
        humid = hum_data['1']

# unpacking soil moisture data
        soil_m_data = pd.read_csv(moist_log, header=None,
        delim_whitespace=True)
        soil_m_data.columns = ['0', '1']
        timestamp_3 = pd.to_datetime(pd.Series(light_data['0']),
        format=time_format)
        moist = soil_m_data['1']

# battery data
        battery = 47

# this section is ready to be deployed in case there's an issue with displaying
# datetime data. May have to specify datemin as something like but at the
# moment that would mess with mock data
#        datemin = datetime.now() - timedelta(hours=24)
#        datemax = datetime.now()
# datemin/max below were dummy in sync with .dat file timestamps
        datemin = datetime(2019, 3, 22, 13, 0, 3)
        datemax = datetime(2019, 3, 22, 13, 10, 4)

        days = dates.DayLocator()
        hours = dates.HourLocator()
        minutes = dates.MinuteLocator()
        seconds = dates.SecondLocator()
        dfmt = dates.DateFormatter('%b %d')
        tmfd = dates.DateFormatter('%H %M')
# setting up how we display data
#        self.mpl.canvas.ax.xaxis.set_major_locator(hours)
#        self.mpl.canvas.ax.xaxis.set_major_formatter(dfmt)
#        self.mpl.canvas.ax.xaxis.set_minor_locator(minutes)
#        self.mpl.canvas.ax.xaxis.set_minor_formatter(tmfd)
#        self.mpl.canvas.ax.set_xlim(datemin, datemax)
#
#        self.mpl.canvas.ax_1.xaxis.set_major_locator(hours)
#        self.mpl.canvas.ax_1.xaxis.set_major_formatter(dfmt)
#        self.mpl.canvas.ax_1.xaxis.set_minor_locator(minutes)
#        self.mpl.canvas.ax_1.xaxis.set_minor_formatter(tmfd)
#        self.mpl.canvas.ax_1.set_xlim(datemin, datemax)
#
#        self.mpl.canvas.ax_1.xaxis.set_major_locator(hours)
#        self.mpl.canvas.ax_1.xaxis.set_major_formatter(dfmt)
#        self.mpl.canvas.ax_1.xaxis.set_minor_locator(minutes)
#        self.mpl.canvas.ax_1.xaxis.set_minor_formatter(tmfd)
#        self.mpl.canvas.ax_2.set_xlim(datemin, datemax)

# ploting temperature data
        self.mpl.canvas.ax.set_ylabel('Temperature ($^\circ$C)')
        self.mpl.canvas.ax.grid(True)
        self.mpl.canvas.ax.plot(timestamp_temp, temp_data.temp_up, c='red', ls=':',
        label='temp_up')
        self.mpl.canvas.ax.plot(timestamp_temp, temp_data.temp_down, c='orange', ls='dotted',
        label='temp_down')
        self.mpl.canvas.ax.plot(timestamp_temp, temp_data.temp_ground, c='brown', ls='-',
        label='ground temperature')
        self.mpl.canvas.ax.fill_between(timestamp_temp, temp_data.temp_up,
        temp_data.temp_down)
        self.mpl.canvas.ax.fill_between(timestamp_temp, temp_data.temp_up, temp_max,
        where=temp_data.temp_up>=temp_max, edgecolor='red', facecolor='none', hatch='/',
        interpolate=True)
        self.mpl.canvas.ax.fill_between(timestamp_temp, temp_data.temp_down, temp_min,
        where=temp_data.temp_down<=temp_min, edgecolor='red', facecolor='none',
        hatch='/', interpolate=True)
        self.mpl.canvas.ax.legend()
# adding light subplot
        self.mpl.canvas.ax_1.set_ylabel('Light lm')
        self.mpl.canvas.ax_1.grid(True)
        self.mpl.canvas.ax_1.plot(timestamp_1, broadband, c='cyan', ls='-.',
        label='broadband')
        self.mpl.canvas.ax_1.plot(timestamp_1, visible, c='orange', ls='-.',
        label='visible')
        self.mpl.canvas.ax_1.plot(timestamp_1, infrared, c='red', ls='-.',
        label='infrared')
        self.mpl.canvas.ax_1.legend()
        self.mpl.canvas.ax_1.fill_between(timestamp_1, broadband, light_max,
        where=broadband>=light_max, edgecolor='red', facecolor='none', hatch="/", interpolate=True)
        self.mpl.canvas.ax_1.fill_between(timestamp_1, broadband, light_min,
        where=broadband<=light_min, edgecolor='red', facecolor='none',
        hatch='/', interpolate=True)

# adding humidity subplot
        self.mpl.canvas.ax_2.set_ylabel('Humidity/watering %')
        self.mpl.canvas.ax_2.grid(True)
        self.mpl.canvas.ax_2.plot(timestamp_2, humid, c='blue', ls='--',
        label='humidity')
# adding to it soil moisture data
        self.mpl.canvas.ax_2.plot(timestamp_3, moist, c='navy', ls=' ',
        label='soil_moisture')
        self.mpl.canvas.ax_2.fill_between(timestamp_2, 0, moist)
        self.mpl.canvas.ax_2.fill_between(timestamp_2, moist, soil_max,
        where=moist>=humid_max, facecolor='none', edgecolor='red', hatch='/', interpolate=True)
        self.mpl.canvas.ax_2.fill_between(timestamp_2, soil_min, moist,
        where=moist<=humid_min, facecolor='none', edgecolor='red', hatch='/',
        interpolate=True)
        self.mpl.canvas.ax_2.legend()
        self.mpl.canvas.ax_3.set_xlabel('Battery level %')
        self.mpl.canvas.ax_3.set_ylim([0, 100])
# should really move those arbitrary values to settings file
        if battery >= 50:
            state = 'g'
        elif 30 < battery < 50:
            state = 'orange'
        else:
            state = 'r'
        self.mpl.canvas.ax_3.bar(1, battery, color = state)
        self.mpl.canvas.ax_3.tick_params(axis='x', which='both', bottom=False,
        labelbottom=False)

# setting up weather station tab:
# adding temperature plot
        self.mpl1.canvas.ax.set_ylabel('Temperature ($^\circ$C)')
        self.mpl1.canvas.ax.grid(True)
        self.mpl1.canvas.ax.plot(timestamp_temp, temp_data.temp_up, c='orange', ls='-.',
        label='temperature outdoors')
# adding light plot
        self.mpl1.canvas.ax_1.set_ylabel('Light lm')
        self.mpl1.canvas.ax_1.grid(True)
        self.mpl1.canvas.ax_1.plot(timestamp_1, visible)
# adding humidity/rainfall graph
# mind you that hist() doesn't do what I'd like it to do. redo.
        self.mpl1.canvas.ax_2.set_ylabel('Humidity/rainfall %')
        self.mpl1.canvas.ax_2.grid(True)
# this is a hack: unit for bar width is days hence hum_data.shape[0] = numbers
# of columns in dataframe allowing for dynamic sizing
        self.mpl1.canvas.ax_2.bar(timestamp_2, humid, width = \
        .01*(1/hum_data.shape[0]), edgecolor = 'black')
        self.mpl1.canvas.ax_3.set_xlabel('Battery level %')
        self.mpl1.canvas.ax_3.set_ylim([0, 100])
        self.mpl1.canvas.ax_3.bar(1, battery, color = state)
        self.mpl1.canvas.ax_3.tick_params(axis='x', which='both', bottom=False,
        labelbottom=False)

# below function reploting graphs called upon detecting user input

    def mpl_replot(self):
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax_1.clear()
        self.mpl.canvas.ax_2.clear()
        self.mpl.canvas.draw_idle()
        self.mplwidget()

# defining warning box
#    def warning_box(QDialog, Ui_Dialog):
#        alert = cfg.getboolean('light', 'bool_alert')
#        if alert == True and light_min < broadband > light_max:
#            self.setupUi(self)

# defining light management ui write actions (could be rewriten, lots of
# redundant code DRY fail big time

    def ui_dialog(self):
        widget = QDialog(self)
        ui = Ui_Dialog()
        ui.setupUi(widget)
        widget.exec_()

    def write_light_trigers(self):
        send_off = str(self.light_trigers_off.isChecked())
        cfg.set('light', 'trigers_off', send_off)
        send_time = str(self.light_trigers_time.isChecked())
        cfg.set('light', 'trigers_clock', send_time)
        send_sensors = str(self.light_trigers_sensors.isChecked())
        cfg.set('light', 'trigers_sensors', send_sensors)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_control(self):
        send_onoff = str(self.light_control_onoff.isChecked())
        cfg.set('light', 'control_onof', send_onoff)
        send_pid = str(self.light_control_pid.isChecked())
        cfg.set('light', 'control_pid', send_pid)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

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

    def write_light_kp(self):
        send = str(self.light_pid_control_kp.value())
        cfg.set('light', 'kp', send)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)


    def write_light_alert(self, state):
        if state == Qt.Checked:
            cfg.set('light', 'bool_alert', 'True')
        else:
            cfg.set('light', 'bool_alert', 'False')

#        send = self.light_bool_alert.value()
#        message = str(send)
#        cfg.set('light', 'light_alert', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

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

    def write_temperature_trigers(self):
        send_off = str(self.temperature_trigers_off.isChecked())
        cfg.set('temperature', 'trigers_off', send_off)
        send_time = str(self.temperature_trigers_time.isChecked())
        cfg.set('temperature', 'trigers_clock', send_time)
        send_sensors = str(self.temperature_trigers_sensors.isChecked())
        cfg.set('temperature', 'trigers_sensors', send_sensors)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

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

    def write_temp_alert(self, state):
        if state == Qt.Checked:
            cfg.set('temperature', 'bool_alert', 'True')
        else:
            pass

# defining humidity management tab

    def write_humidity_trigers(self):
        send_off = str(self.humidity_trigers_off.isChecked())
        cfg.set('humidity', 'trigers_off', send_off)
        send_sensors = str(self.humidity_trigers_sensors.isChecked())
        cfg.set('humidity', 'trigers_sensors', send_sensors)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_hum_min(self):
        send = self.humidity_humidity_min.value()
        message = str(send)
        cfg.set('humidity', 'humidity_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_hum_max(self):
        send = self.humidity_humidity_max.value()
        message = str(send)
        cfg.set('humidity', 'humidity_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_humidity_bool_alert(self, state):
        if state == Qt.Checked:
            cfg.set('humidity', 'bool_alert', 'True')
        else:
            cfg.set('humidity', 'bool_alert', 'False')
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

# defining water management tab

    def write_water_trigers(self):
        send_off = str(self.water_trigers_off.isChecked())
        cfg.set('water', 'trigers_off', send_off)
        send_time = str(self.water_trigers_time.isChecked())
        cfg.set('water', 'trigers_clock', send_time)
        send_sensors = str(self.water_trigers_sensors.isChecked())
        cfg.set('water', 'trigers_sensors', send_sensors)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_soil_moisture_min(self):
        send = self.water_soil_moisture_min.value()
        message = str(send)
        cfg.set('water', 'soil_moisture_min', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_soil_moisture_max(self):
        send = self.water_soil_moisture_max.value()
        message = str(send)
        cfg.set('water', 'soil_moisture_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_water_bool_alert(self, state):
        if state == Qt.Checked:
            cfg.set('water', 'bool_alert', 'True')
        else:
            cfg.set('water', 'bool_alert', 'False')
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_watering_time(self):
        send = self.water_time_of_watering.time()
        message = send.toString(self.water_time_of_watering.displayFormat())
        cfg.set('water', 'time_of_watering', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_watering_duration(self):
        send = self.water_time_watering_duration.time()
        message = send.toString(self.water_time_of_watering.displayFormat())
        cfg.set('water', 'time_watering_duration', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

    def write_watering_amount(self):
        send = self.water_amount.value()
        message = str(send)
        cfg.set('water', 'amount', message)
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
