#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import dates
import numpy as np
import pandas as pd
import configparser
from RPGH_main_gui_signals_sorted import Ui_MainWindow

sys.path.append('..')
LOCAL_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

config_f = 'settings_config_parser.py'
cfg = configparser.ConfigParser()
cfg.read('settings_config_parser.py')

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.replot_pushButton.clicked.connect(self.mpl_replot)
        self.temperature_temp_max.setValue(cfg.getint('temperature', 'temp_max'))
        self.temperature_temp_max.valueChanged.connect(self.write_temp_max)
        self.mplwidget()

    def mplwidget(self):
        temp_max = cfg.getint('temperature', 'temp_max')
        temp_log = 'sensor_logs/temperature_out.dat'
        time_format = '%d,%m,%Y,%X'
        temp_data = pd.read_csv(temp_log, header=None, delim_whitespace=True)
        temp_data.columns = ['timestamp', 'temp_up', 'temp_down',
        'temp_ground']
        timestamp = pd.to_datetime(pd.Series(temp_data.timestamp),
        format=time_format)
        self.mpl.canvas.ax.plot(timestamp, temp_data.temp_up)
        self.mpl.canvas.ax.fill_between(timestamp, temp_data.temp_up, temp_max,
        where=temp_data.temp_up>=temp_max, edgecolor='red', facecolor='none',
        hatch='/', interpolate=True)

    def mpl_replot(self):
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.draw_idle()
        self.mplwidget()

    def write_temp_max(self):
        send = self.temperature_temp_max.value()
        message = str(send)
        cfg.set('temperature', 'temp_max', message)
        with open(config_f, 'w') as conffile:
            cfg.write(conffile)

if __name__ == '__main__':

    app = QtWidgets.QApplication([sys.argv])
    gui = DesignerMainWindow()
    gui.show()
    sys.exit(app.exec_())
