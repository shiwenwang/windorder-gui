from PyQt5.QtWidgets import QWidget, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class PlotWidget(QWidget):
    def __init__(self, inputs):
        super(PlotWidget, self).__init__(None)
        # self.ref_wind = ref_wind
        # self.wind_file_name = wind_file_name

        plt.close()

        self.figure = plt.figure(figsize=(9, 5))
        self.bar_plot, self.data = inputs
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.setLayout(layout)
        self.setWindowTitle('风参排序')
    
    def plot(self):
        ul_data = self.data['ul']
        fl_data = self.data['fl']

        self.bar_plot(self.figure, ul_data, 211)
        self.bar_plot(self.figure, fl_data, 212)

        plt.tight_layout()
        
        # refresh canvas
        self.canvas.draw()
