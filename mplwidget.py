#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is matplotlib widget.
Author: uinarf
Date: 21.05.2019
"""


from PyQt5 import QtGui
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as \
NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import gridspec

#matplotlib.use('QT5Agg')

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(tight_layout=True)
        grid = gridspec.GridSpec(ncols=32, nrows=3)
        self.ax = self.fig.add_subplot(grid[0, 0:30])
        self.ax_1 = self.fig.add_subplot(grid[1, 0:30])
        self.ax_2 = self.fig.add_subplot(grid[2, 0:30])
        self.ax_3 = self.fig.add_subplot(grid[0:, 31])
        self.fig.align_labels()
#        self.ax = self.fig.add_subplot(311)
#        self.ax_1 = self.fig.add_subplot(312)
#        self.ax_2 = self.fig.add_subplot(313)
#        self.ax_3 = self.fig.add_subplot(321)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
