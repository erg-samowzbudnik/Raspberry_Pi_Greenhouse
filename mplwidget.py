from PyQt5 import QtGui
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QHBoxLayout()
       # self.setLayout(self.vbl)
        #self.layout = QtWidgets.QHBoxLayout()
        #self.layout.addLayout(self.vbl,0)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

#class MplWidget(QtWidgets.QWidget):
#    def __init__(self, parent = None):
#        QtWidgets.QWidget.__init__(self, parent)
#        self.canvas = MplCanvas()
#        self.vbl = QtWidgets.QVBoxLayout()
#        self.vbl.addLayout(self.canvas)
#        self.setLayout(self.vbl)

