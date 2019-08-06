# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from ui_mainwindow import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
