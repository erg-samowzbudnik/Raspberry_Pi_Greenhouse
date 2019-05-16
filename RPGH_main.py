#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# the ui file barfs because defined there mplwidget is not.
# now I wrote the widget. thing barfs at the way we load the UI so here I'll
# rewrite just the way it loads UI

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
from Tab_Widget_Main_scailing_01 import Ui_MainWindow

sys.path.append('..')

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

# read and extract/format configuration data
config_f = 'settings_config_parser.py'
cfg = configparser.ConfigParser()
cfg.read('settings_config_parser.py')

# light management
light_min = cfg.getint('light', 'light_min')
light_max = cfg.getint('light', 'light_max')

light_time_on_to_convert = cfg.get('light', 'light_time_on')
light_time_on = datetime.strptime(light_time_on_to_convert, '%H:%M').time()

light_time_off_to_convert = cfg.get('light', 'light_time_off')
light_time_off = datetime.strptime(light_time_off_to_convert, '%H:%M').time()

light_rgb_red = cfg.getint('light', 'light_rgb_red')
light_rgb_green = cfg.getint('light', 'light_rgb_green')
light_rgb_blue = cfg.getint('light', 'light_rgb_blue')
light_normalise = cfg.getboolean('light', 'light_normalise')

light_alert = cfg.getboolean('light', 'light_normalise')

# temperature managenent
temp_min = cfg.getint('temperature', 'temp_min')
temp_max = cfg.getint('temperature', 'temp_max')

temp_heating_on_to_convert = cfg.get('temperature', 'temp_heating_on')
temp_heating_on = datetime.strptime(temp_heating_on_to_convert, '%H:%M').time()

temp_heating_off_to_convert = cfg.get('temperature', 'temp_heating_off')
temp_heating_off = datetime.strptime(temp_heating_off_to_convert, '%H:%M').time()

temp_venting_on_to_convert = cfg.get('temperature', 'temp_venting_on')
temp_venting_on = datetime.strptime(temp_venting_on_to_convert, '%H:%M').time()

temp_venting_off_to_convert = cfg.get('temperature', 'temp_venting_off')
temp_venting_off = datetime.strptime(temp_venting_off_to_convert, '%H:%M').time()

temp_normalise = cfg.getboolean('temperature', 'temp_normalise')
temp_alert = cfg.getboolean('temperature', 'temp_alert')


fq = cfg.getfloat('hardware_settings', 'read_frequency')

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        #self.ui = uic.loadUi(LOCAL_DIR + "Tab_Widget_main_GUI_03.ui", self)

# setting up light management tab
        self.light_light_min.setValue(light_min)
        self.light_light_min.valueChanged.connect(self.write_light_min)

        self.light_light_max.setValue(light_max)
        self.light_light_max.valueChanged.connect(self.write_light_max)

        self.light_rgb_red.setValue(light_rgb_red)
        self.light_rgb_red.valueChanged.connect(self.write_light_rgb_red)

        self.light_rgb_green.setValue(light_rgb_green)
        self.light_rgb_green.valueChanged.connect(self.write_light_rgb_green)

        self.light_rgb_blue.setValue(light_rgb_blue)
        self.light_rgb_blue.valueChanged.connect(self.write_light_rgb_green)

#        self.light_bool_normalise.setChecked(light_normalise)
#        self.light_bool_normalise.isChecked(light_normalise)
#
#        self.light_bool_alert.setChecked(light_alert)

        self.light_time_on.setTime(light_time_on)
        self.light_time_on.timeChanged.connect(self.write_light_time_on)

        self.light_time_off.setTime(light_time_off)
        self.light_time_off.timeChanged.connect(self.write_light_time_off)

# setting up temperature management tab

        self.temperature_temp_min.setValue(temp_min)
        self.temperature_temp_min.valueChanged.connect(self.write_temp_min)

        self.temperature_temp_max.setValue(temp_max)
        self.temperature_temp_max.valueChanged.connect(self.write_temp_max)

        self.temperature_time_heating_on.setTime(temp_heating_on)
        self.temperature_time_heating_on.timeChanged.connect(self.write_temp_heating_time_on)

        self.temperature_time_heating_off.setTime(temp_heating_off)
        self.temperature_time_heating_off.timeChanged.connect(self.write_temp_heating_time_off)

        self.temperature_time_venting_on.setTime(temp_venting_on)
        self.temperature_time_venting_on.timeChanged.connect(self.write_temp_vent_time_on)

        self.temperature_time_venting_off.setTime(temp_venting_off)
        self.temperature_time_venting_off.timeChanged.connect(self.write_temp_vent_time_off)

# setting up humidity management tab

    def mplwidget(self):
        timestamp = np.array([])
        temp_up = np.array([])
        temp_down = np.array([])
        time_format = '%d,%m,%Y,%X'

        with open('temperature_out.dat', 'r') as temperature:
            for i, line in enumerate(temperature):
                a, b, c = line.split(' ')
                timestamp.append(datetime.strptime(a, time_format))
                temp_up.append(float(b))
                temp_down.append(float(c))


        datemin = datetime(2019, 3, 22, 13, 0, 3)
        datemax = datetime(2019, 3, 22, 13, 10, 4)

        days = dates.DayLocator()
        hours = dates.HourLocator()
        minutes = dates.MinuteLocator()
        seconds = dates.SecondLocator()
        dfmt = dates.DateFormatter('%b %d')
        tmfd = dates.DateFormatter('%H %M')

        self.canvas.ax.plot(timestamp, temp_up)
        self.canvas.draw()
#        self.mpl.canvas.ax.clear()
#        self.mpl.canvas.ax.xaxis.set_major_loactor(hours)
#        self.mpl.canvas.ax.xaxis.set_major_formater(dmft)
#        self.mpl.canvas.ax.xaxis.set_minor_formater(tmfd)
#        self.mpl.canvas.ax.xaxis.set_minor_locator(minutes)
#        self.mpl.canvas.ax.set_xlim(datemin, datemax)
#        self.mpl.canvas.ax.set_ylabel('temperature (C)')
#        self.mpl.canvas.ax.set_xlabel('Time')
#        self.mpl.canvas.ax.grid(True)
#        self.mpl.canvas.ax.plot(timestamp, temp_up, c='red', ls='dashed')
#        self.mpl.canvas.ax.plot(timestamp,temp_down, c='orange', ls='dotted')
#        self.mpl.canvas.ax.fill_between(timestamp, temp_up, temp_down)
#        self.mpl.canvas.draw()
# defining light management ui


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

    def write_light_normalise(self):
        send = self.light_bool_normalise.value()
        message = str(send)
        cfg.set('light', 'light_normalise', message)
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
