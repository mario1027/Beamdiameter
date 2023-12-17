import sys
import matplotlib
matplotlib.use('Qt5Agg') 

from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height))
        self.fig.subplots_adjust(wspace=0.3,left=0,right=0.75)
        self.ax = self.fig.add_subplot(111)
        
        super(MplCanvas, self).__init__(self.fig)


class plot2dW(QtWidgets.QMainWindow):
    def __init__(self,laser_data):
        super().__init__()
        
        sc = MplCanvas(self, width=8, height=4, dpi=100)
        laser_data.plot2dworkax(sc)
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

