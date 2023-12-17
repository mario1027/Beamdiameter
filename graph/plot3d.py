import sys
import matplotlib
matplotlib.use('Qt5Agg') 
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas3d(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        fig = Figure(figsize=(18,14))
        self.axes = fig.add_subplot(projection='3d')
        super(MplCanvas3d, self).__init__(fig)





class plot3d(QtWidgets.QMainWindow):
                def __init__(self,image):
                    super().__init__()
                    v11,h11 = image.shape
                    X11, Y11 = np.meshgrid(range(h11), range(v11))
                    hmax=image.max()
                    X, Y, Z = X11,Y11,image/hmax
                    sc = MplCanvas3d(self)
                    sc.axes.plot_surface(X, Y, Z,cmap='turbo')
                    sc.axes.contourf(X, Y, Z, zdir='z', offset=-1.2, cmap='turbo')
                    sc.axes.contour(X, Y, Z, zdir='x', offset=0, cmap='jet')
                    sc.axes.contour(X, Y, Z, zdir='y', offset=np.max(Y), cmap='jet')
                    sc.axes.set_zlim(-1.2, np.max(Z))
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
                    