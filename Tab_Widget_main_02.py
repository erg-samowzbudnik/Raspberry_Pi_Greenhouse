#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick, uic
import configparser

sys.path.append('..')

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

cfg = configparser.ConfigParser()
cfg.read('settings_config_parser.py')   # reading defaults and settings from the file

fq = cfg.getfloat('hardware_settings', 'read_frequency')
light_min = cfg.getint('light', 'light_min')
light_max = cfg.getint('light', 'light_max')
light_on = cfg.get('light', 'light_on') # this has wrong format for timeEdit



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(LOCAL_DIR + "Tab_Widget_main_GUI_02.ui", self)
        
        # setting up gnuplot
        gnuplot_path = r'/usr/bin/gnuplot'
        #self.ui.QtQuick.QQuickView = QQuickView()
        win = QtWidgets.QWidget()
        winID = int(win.winId())
        sub_win = QtGui.QWindow.fromWinId(winID)
        container = QtWidgets.QWidget.createWindowContainer(sub_win)
        sub_win_id = int(container.winId())
        process = QtCore.QProcess(container)
        
        #self.ui.widget_2.createWindowContainer(sub_win)
        #self.ui.quickWidget(self.set_up_gnuplot)
        #self.ui.widget_2.createWindowContainer()
        #self.ui.createWindowContainer()
        self.process = QtCore.QProcess(self)
        self.process.start(gnuplot_path, ["-p gnuplot_greenhouse.conf"])
        
        
        # setting up light management part
        # setting up light->sensors->min
        self.ui.spinBox_13_light_min.setValue(light_min)
        self.ui.spinBox_13_light_min.valueChanged.connect(self.write_light_min)
        # setting up light->sensors->max
        self.ui.spinBox_14_light_max.setValue(light_max)
        self.ui.spinBox_14_light_max.valueChanged.connect(self.write_light_max)
        # setting up light->sensors->time_on
        #self.ui.timeEdit_11.setTime(light_on)
        #self.ui.timeEdit_11.timeChanged.connect(write_light_on)
        # setting up light->sensors->time_off

        # setting up user_settings->hardware_settings->sensor_read_frequency
        self.ui.doubleSpinBox_frequency.setValue(fq)
        self.ui.doubleSpinBox_frequency.valueChanged.connect(self.write_fq)
        self.show()

    def set_up_gnuplot(self):
        self.ui.Qprocess(gnuplot_path, ["-p gnuplot_greenhouse.conf"])
        return



    def write_light_min(self):
        send = self.ui.spinBox_13_light_min.value()
        message = str(send)
        cfg.set('light', 'light_min', message)
        with open('settings_config_parser.py', 'w') as conffile:
            cfg.write(conffile)
        return

    def write_light_max(self):
        send = self.ui.spinBox_14_light_max.value()
        message = str(send)
        cfg.set('light', 'light_max', message)
        with open('settings_config_parser.py', 'w') as conffile:
            cfg.write(conffile)
        return

    def write_light_on(self):
        send = self.ui.timeEdit_11.value()
        message = str(send)
        cfg.set('light', 'light_on', message)
        with open('settings_config_parser.py', 'w') as conffile:
            cfg.write(conffile)
        return

    def write_fq(self):
        send = self.ui.doubleSpinBox_frequency.value()
        message = str(send)
        cfg.set('hardware_settings', 'read_frequency', message)
        with open('settings_config_parser.py', 'w') as conffile:
            cfg.write(conffile)
        return

if __name__ == '__main__':
    app = QtWidgets.QApplication([sys.argv])
    gui = App()
    sys.exit(app.exec_())
