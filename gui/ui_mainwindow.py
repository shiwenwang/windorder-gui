# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\WorkSpace\6_Programming\wind_order\qt\wind_order\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!
from json import JSONDecodeError

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from functools import partial
import os
import sys
import time

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(THIS_DIR, '..')))
from core import TowerDataBase, main_run, find_available_tower, compare, MySQLDataBase, MyFTP
# import wind_cmp, windorder
from gui.ui_widget import *
import json

IMG_PATH = os.path.abspath(os.path.join(THIS_DIR, './res/img/'))


class Ui_MainWindow(object):
    def __init__(self):
        self.version = '1.2.0'
        self.tower_sql = MySQLDataBase()
        self.loads = {}
        self.selected_towers = []
        self.rec_last_selected_towers = []
        self.last_available_tower = []
        self.wind_info = {}
        self.tower_info = {}
        self.connect_state = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 511)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./sort_ico.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_8.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.groupBox_farm = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_farm.sizePolicy().hasHeightForWidth())
        self.groupBox_farm.setSizePolicy(sizePolicy)
        self.groupBox_farm.setMinimumSize(QtCore.QSize(450, 70))
        font = QtGui.QFont()
        font.setUnderline(False)
        self.groupBox_farm.setFont(font)
        self.groupBox_farm.setFlat(False)
        self.groupBox_farm.setCheckable(False)
        self.groupBox_farm.setObjectName("groupBox_farm")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_farm)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_farm = QtWidgets.QGridLayout()
        self.gridLayout_farm.setSpacing(6)
        self.gridLayout_farm.setObjectName("gridLayout_farm")
        self.lineEdit_farm = MyLineEdit(self.groupBox_farm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_farm.sizePolicy().hasHeightForWidth())
        self.lineEdit_farm.setSizePolicy(sizePolicy)
        self.lineEdit_farm.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_farm.setFont(font)
        self.lineEdit_farm.setObjectName("lineEdit_farm")
        self.gridLayout_farm.addWidget(self.lineEdit_farm, 0, 0, 1, 1)
        self.pushButton_farm = QtWidgets.QPushButton(self.groupBox_farm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_farm.sizePolicy().hasHeightForWidth())
        self.pushButton_farm.setSizePolicy(sizePolicy)
        self.pushButton_farm.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_farm.setObjectName("pushButton_farm")
        self.gridLayout_farm.addWidget(self.pushButton_farm, 0, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_farm, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_farm, 0, 0, 1, 1)
        self.groupBox_ref_path = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_ref_path.sizePolicy().hasHeightForWidth())
        self.groupBox_ref_path.setSizePolicy(sizePolicy)
        self.groupBox_ref_path.setMinimumSize(QtCore.QSize(450, 100))
        self.groupBox_ref_path.setCheckable(True)
        self.groupBox_ref_path.setObjectName("groupBox_ref_path")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_ref_path)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_std = QtWidgets.QHBoxLayout()
        self.horizontalLayout_std.setSpacing(6)
        self.horizontalLayout_std.setObjectName("horizontalLayout_std")
        self.label_ref_std = QtWidgets.QLabel(self.groupBox_ref_path)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_ref_std.setFont(font)
        self.label_ref_std.setObjectName("label_ref_std")
        self.horizontalLayout_std.addWidget(self.label_ref_std)
        self.lineEdit_ref_std = MyLineEdit(self.groupBox_ref_path)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ref_std.sizePolicy().hasHeightForWidth())
        self.lineEdit_ref_std.setSizePolicy(sizePolicy)
        self.lineEdit_ref_std.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_ref_std.setObjectName("lineEdit_ref_std")
        self.horizontalLayout_std.addWidget(self.lineEdit_ref_std)
        self.pushButton_ref_std = QtWidgets.QPushButton(self.groupBox_ref_path)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ref_std.sizePolicy().hasHeightForWidth())
        self.pushButton_ref_std.setSizePolicy(sizePolicy)
        self.pushButton_ref_std.setMinimumSize(QtCore.QSize(0, 25))
        self.pushButton_ref_std.setObjectName("pushButton_ref_std")
        self.horizontalLayout_std.addWidget(self.pushButton_ref_std)
        self.gridLayout_3.addLayout(self.horizontalLayout_std, 1, 0, 1, 1)
        self.horizontalLayout_cz = QtWidgets.QHBoxLayout()
        self.horizontalLayout_cz.setSpacing(6)
        self.horizontalLayout_cz.setObjectName("horizontalLayout_cz")
        self.label_ref_cz = QtWidgets.QLabel(self.groupBox_ref_path)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_ref_cz.setFont(font)
        self.label_ref_cz.setObjectName("label_ref_cz")
        self.horizontalLayout_cz.addWidget(self.label_ref_cz)
        self.lineEdit_ref_cz = MyLineEdit(self.groupBox_ref_path)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ref_cz.sizePolicy().hasHeightForWidth())
        self.lineEdit_ref_cz.setSizePolicy(sizePolicy)
        self.lineEdit_ref_cz.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_ref_cz.setObjectName("lineEdit_ref_cz")
        self.horizontalLayout_cz.addWidget(self.lineEdit_ref_cz)
        self.pushButton_ref_cz = QtWidgets.QPushButton(self.groupBox_ref_path)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_ref_cz.sizePolicy().hasHeightForWidth())
        self.pushButton_ref_cz.setSizePolicy(sizePolicy)
        self.pushButton_ref_cz.setMinimumSize(QtCore.QSize(0, 25))
        self.pushButton_ref_cz.setObjectName("pushButton_ref_cz")
        self.horizontalLayout_cz.addWidget(self.pushButton_ref_cz)
        self.gridLayout_3.addLayout(self.horizontalLayout_cz, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_ref_path, 1, 0, 1, 1)
        self.groupBox_turbine_lib = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_turbine_lib.sizePolicy().hasHeightForWidth())
        self.groupBox_turbine_lib.setSizePolicy(sizePolicy)
        self.groupBox_turbine_lib.setMinimumSize(QtCore.QSize(450, 250))
        self.groupBox_turbine_lib.setCheckable(True)
        self.groupBox_turbine_lib.setObjectName("groupBox_turbine_lib")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_turbine_lib)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_tower_list = QtWidgets.QGroupBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_tower_list.sizePolicy().hasHeightForWidth())
        self.groupBox_tower_list.setSizePolicy(sizePolicy)
        self.groupBox_tower_list.setWhatsThis("")
        self.groupBox_tower_list.setObjectName("groupBox_tower_list")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_tower_list)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.listWidget_towers_list = QtWidgets.QListWidget(self.groupBox_tower_list)
        self.listWidget_towers_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_towers_list.setObjectName("listWidget_towers_list")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_towers_list.addItem(item)
        self.gridLayout_5.addWidget(self.listWidget_towers_list, 0, 0, 2, 1)
        self.checkBox_select_all = QtWidgets.QCheckBox(self.groupBox_tower_list)
        self.checkBox_select_all.setObjectName("checkBox_select_all")
        self.gridLayout_5.addWidget(self.checkBox_select_all, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_tower_list, 2, 0, 1, 1)
        self.gridLayout_attr = QtWidgets.QGridLayout()
        self.gridLayout_attr.setSpacing(6)
        self.gridLayout_attr.setObjectName("gridLayout_attr")
        self.label_turbine = QtWidgets.QLabel(self.groupBox_turbine_lib)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_turbine.setFont(font)
        self.label_turbine.setObjectName("label_turbine")
        self.gridLayout_attr.addWidget(self.label_turbine, 0, 0, 1, 1)
        self.comboBox_turbine = QtWidgets.QComboBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_turbine.sizePolicy().hasHeightForWidth())
        self.comboBox_turbine.setSizePolicy(sizePolicy)
        self.comboBox_turbine.setMinimumSize(QtCore.QSize(0, 20))
        self.comboBox_turbine.setObjectName("comboBox_turbine")
        self.gridLayout_attr.addWidget(self.comboBox_turbine, 0, 1, 1, 1)
        self.label_hubheight = QtWidgets.QLabel(self.groupBox_turbine_lib)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_hubheight.setFont(font)
        self.label_hubheight.setObjectName("label_hubheight")
        self.gridLayout_attr.addWidget(self.label_hubheight, 0, 2, 1, 1)
        self.comboBox_hubheight = QtWidgets.QComboBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_hubheight.sizePolicy().hasHeightForWidth())
        self.comboBox_hubheight.setSizePolicy(sizePolicy)
        self.comboBox_hubheight.setMinimumSize(QtCore.QSize(0, 20))
        self.comboBox_hubheight.setObjectName("comboBox_hubheight")
        self.gridLayout_attr.addWidget(self.comboBox_hubheight, 0, 3, 1, 1)
        self.label_blade = QtWidgets.QLabel(self.groupBox_turbine_lib)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_blade.setFont(font)
        self.label_blade.setObjectName("label_blade")
        self.gridLayout_attr.addWidget(self.label_blade, 1, 0, 1, 1)
        self.comboBox_blade = QtWidgets.QComboBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_blade.sizePolicy().hasHeightForWidth())
        self.comboBox_blade.setSizePolicy(sizePolicy)
        self.comboBox_blade.setMinimumSize(QtCore.QSize(0, 20))
        self.comboBox_blade.setObjectName("comboBox_blade")
        self.gridLayout_attr.addWidget(self.comboBox_blade, 1, 1, 1, 1)
        self.comboBox_custom_key = QtWidgets.QComboBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_custom_key.sizePolicy().hasHeightForWidth())
        self.comboBox_custom_key.setSizePolicy(sizePolicy)
        self.comboBox_custom_key.setMinimumSize(QtCore.QSize(0, 20))
        self.comboBox_custom_key.setObjectName("comboBox_custom_key")
        self.gridLayout_attr.addWidget(self.comboBox_custom_key, 1, 2, 1, 1)
        self.comboBox_custom_value = QtWidgets.QComboBox(self.groupBox_turbine_lib)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_custom_value.sizePolicy().hasHeightForWidth())
        self.comboBox_custom_value.setSizePolicy(sizePolicy)
        self.comboBox_custom_value.setMinimumSize(QtCore.QSize(0, 20))
        self.comboBox_custom_value.setObjectName("comboBox_custom_value")
        self.gridLayout_attr.addWidget(self.comboBox_custom_value, 1, 3, 1, 1)
        self.gridLayout_attr.setColumnStretch(1, 1)
        self.gridLayout_attr.setColumnStretch(3, 1)
        self.gridLayout.addLayout(self.gridLayout_attr, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_turbine_lib)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.checkBox_turbine = QtWidgets.QCheckBox(self.groupBox_turbine_lib)
        self.checkBox_turbine.setObjectName("checkBox_turbine")
        self.horizontalLayout.addWidget(self.checkBox_turbine)
        self.checkBox_blade = QtWidgets.QCheckBox(self.groupBox_turbine_lib)
        self.checkBox_blade.setObjectName("checkBox_blade")
        self.horizontalLayout.addWidget(self.checkBox_blade)
        self.checkBox_hubheight = QtWidgets.QCheckBox(self.groupBox_turbine_lib)
        self.checkBox_hubheight.setObjectName("checkBox_hubheight")
        self.horizontalLayout.addWidget(self.checkBox_hubheight)
        self.checkBox_custom = QtWidgets.QCheckBox(self.groupBox_turbine_lib)
        self.checkBox_custom.setObjectName("checkBox_devtype")
        self.horizontalLayout.addWidget(self.checkBox_custom)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_reset = QtWidgets.QPushButton(self.groupBox_turbine_lib)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout_2.addWidget(self.pushButton_reset)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_turbine_lib, 2, 0, 2, 1)
        self.groupBox_functools = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_functools.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_functools.sizePolicy().hasHeightForWidth())
        self.groupBox_functools.setSizePolicy(sizePolicy)
        self.groupBox_functools.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_functools.setObjectName("groupBox_functools")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_functools)
        self.gridLayout_9.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pushButton_towerrec = QtWidgets.QPushButton(self.groupBox_functools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_towerrec.sizePolicy().hasHeightForWidth())
        self.pushButton_towerrec.setSizePolicy(sizePolicy)
        self.pushButton_towerrec.setMinimumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_towerrec.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./reco_btn.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_towerrec.setIcon(icon1)
        self.pushButton_towerrec.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_towerrec.setObjectName("pushButton_towerrec")
        self.gridLayout_9.addWidget(self.pushButton_towerrec, 0, 1, 1, 1)
        self.pushButton_export = QtWidgets.QPushButton(self.groupBox_functools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_export.sizePolicy().hasHeightForWidth())
        self.pushButton_export.setSizePolicy(sizePolicy)
        self.pushButton_export.setMinimumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.pushButton_export.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./export_btn.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_export.setIcon(icon2)
        self.pushButton_export.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_export.setObjectName("pushButton_export")
        self.gridLayout_9.addWidget(self.pushButton_export, 0, 2, 1, 1)
        self.pushButton_sort = QtWidgets.QPushButton(self.groupBox_functools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_sort.sizePolicy().hasHeightForWidth())
        self.pushButton_sort.setSizePolicy(sizePolicy)
        self.pushButton_sort.setMinimumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_sort.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./sort_btn.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_sort.setIcon(icon3)
        self.pushButton_sort.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_sort.setObjectName("pushButton_sort")
        self.gridLayout_9.addWidget(self.pushButton_sort, 0, 0, 1, 1)
        self.gridLayout_9.setColumnStretch(0, 1)
        self.gridLayout_8.addWidget(self.groupBox_functools, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem2, 0, 2, 1, 1)
        self.groupBox_tower_result = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_tower_result.sizePolicy().hasHeightForWidth())
        self.groupBox_tower_result.setSizePolicy(sizePolicy)
        self.groupBox_tower_result.setMinimumSize(QtCore.QSize(332, 360))
        self.groupBox_tower_result.setObjectName("groupBox_tower_result")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_tower_result)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_result = QtWidgets.QTabWidget(self.groupBox_tower_result)
        self.tabWidget_result.setObjectName("tabWidget_result")
        self.tab_tower = QtWidgets.QWidget()
        self.tab_tower.setObjectName("tab_tower")
        self.gridLayout_tower = QtWidgets.QGridLayout(self.tab_tower)
        self.gridLayout_tower.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_tower.setSpacing(6)
        self.gridLayout_tower.setObjectName("gridLayout_tower")
        self.tableWidget_tower_result = QtWidgets.QTableWidget(self.tab_tower)
        self.tableWidget_tower_result.setRowCount(0)
        self.tableWidget_tower_result.setColumnCount(0)
        self.tableWidget_tower_result.setObjectName("tableWidget_tower_result")
        self.gridLayout_tower.addWidget(self.tableWidget_tower_result, 0, 0, 1, 1)
        self.tabWidget_result.addTab(self.tab_tower, "")
        self.tab_condition = QtWidgets.QWidget()
        self.tab_condition.setObjectName("tab_condition")
        self.gridLayout_condition = QtWidgets.QGridLayout(self.tab_condition)
        self.gridLayout_condition.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_condition.setSpacing(6)
        self.gridLayout_condition.setObjectName("gridLayout_condition")
        self.tableWidget_condition = QtWidgets.QTableWidget(self.tab_condition)
        self.tableWidget_condition.setObjectName("tableWidget_condition")
        self.tableWidget_condition.setColumnCount(0)
        self.tableWidget_condition.setRowCount(0)
        self.gridLayout_condition.addWidget(self.tableWidget_condition, 0, 0, 1, 1)
        self.tabWidget_result.addTab(self.tab_condition, "")
        self.tab_m1 = QtWidgets.QWidget()
        self.tab_m1.setObjectName("tab_m1")
        self.gridLayout_m1 = QtWidgets.QGridLayout(self.tab_m1)
        self.gridLayout_m1.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_m1.setSpacing(6)
        self.gridLayout_m1.setObjectName("gridLayout_m1")
        self.tableWidget_m1 = QtWidgets.QTableWidget(self.tab_m1)
        self.tableWidget_m1.setObjectName("tableWidget_m1")
        self.tableWidget_m1.setColumnCount(0)
        self.tableWidget_m1.setRowCount(0)
        self.gridLayout_m1.addWidget(self.tableWidget_m1, 0, 0, 1, 1)
        self.tabWidget_result.addTab(self.tab_m1, "")
        self.tab_m10 = QtWidgets.QWidget()
        self.tab_m10.setObjectName("tab_m10")
        self.gridLayout_m10 = QtWidgets.QGridLayout(self.tab_m10)
        self.gridLayout_m10.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_m10.setSpacing(6)
        self.gridLayout_m10.setObjectName("gridLayout_m10")
        self.tableWidget_m10 = QtWidgets.QTableWidget(self.tab_m1)
        self.tableWidget_m10.setObjectName("tableWidget_m10")
        self.tableWidget_m10.setColumnCount(0)
        self.tableWidget_m10.setRowCount(0)
        self.gridLayout_m10.addWidget(self.tableWidget_m10, 0, 0, 1, 1)
        self.tabWidget_result.addTab(self.tab_m10, "")
        self.tab_etm = QtWidgets.QWidget()
        self.tab_etm.setObjectName("tab_etm")
        self.gridLayout_etm = QtWidgets.QGridLayout(self.tab_etm)
        self.gridLayout_etm.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_etm.setSpacing(6)
        self.gridLayout_etm.setObjectName("gridLayout_etm")
        self.tableWidget_etm = QtWidgets.QTableWidget(self.tab_etm)
        self.tableWidget_etm.setObjectName("tableWidget_etm")
        self.tableWidget_etm.setColumnCount(0)
        self.tableWidget_etm.setRowCount(0)
        self.gridLayout_etm.addWidget(self.tableWidget_etm, 0, 0, 1, 1)
        self.tabWidget_result.addTab(self.tab_etm, "")
        self.gridLayout_2.addWidget(self.tabWidget_result, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_tower_result, 1, 1, 3, 2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 812, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu_file = QtWidgets.QMenu(self.menuBar)
        self.menu_file.setObjectName("menu_file")
        self.menu_database = QtWidgets.QMenu(self.menuBar)
        self.menu_database.setObjectName("menu_database")
        self.menu_tools = QtWidgets.QMenu(self.menuBar)
        self.menu_tools.setObjectName("menu_tools")
        self.menu_help = QtWidgets.QMenu(self.menuBar)
        self.menu_help.setObjectName("menu_help")
        MainWindow.setMenuBar(self.menuBar)
        self.action_openfile = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./open_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_openfile.setIcon(icon4)
        self.action_openfile.setObjectName("action_openfile")
        self.action_deletefile = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./clear_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_deletefile.setIcon(icon5)
        self.action_deletefile.setObjectName("action_deletefile")
        self.action_exit = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./exit_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_exit.setIcon(icon6)
        self.action_exit.setObjectName("action_exit")
        self.action_db_connect = QtWidgets.QAction(MainWindow)
        icon_connect = QtGui.QIcon()
        icon_connect.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./connect_act.png")), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)
        self.action_db_connect.setIcon(icon_connect)
        self.action_db_connect.setObjectName("action_db_connect")
        self.action_db_config = QtWidgets.QAction(MainWindow)
        icon_config = QtGui.QIcon()
        icon_config.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./config_act.png")), QtGui.QIcon.Normal,
                              QtGui.QIcon.Off)
        self.action_db_config.setIcon(icon_config)
        self.action_db_config.setObjectName("action_db_config")
        self.action_sort = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./sort_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_sort.setIcon(icon7)
        self.action_sort.setObjectName("action_sort")
        self.action_towerrec = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./reco_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_towerrec.setIcon(icon8)
        self.action_towerrec.setObjectName("action_towerrec")
        self.action_update = QtWidgets.QAction(MainWindow)
        icon_update = QtGui.QIcon()
        icon_update.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./update.png")),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_update.setIcon(icon_update)
        self.action_update.setObjectName("action_update")
        self.action_contact = QtWidgets.QAction(MainWindow)
        icon_contact = QtGui.QIcon()
        icon_contact.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./help.png")),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_contact.setIcon(icon_contact)
        self.action_contact.setObjectName("action_contact")
        self.action_about = QtWidgets.QAction(MainWindow)
        icon_about = QtGui.QIcon()
        icon_about.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./about.png")), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)
        self.action_about.setIcon(icon_about)
        self.action_about.setObjectName("action_about")

        self.action_export = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./export_act.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_export.setIcon(icon9)
        self.action_export.setObjectName("action_export")
        self.menu_file.addAction(self.action_openfile)
        self.menu_file.addAction(self.action_deletefile)
        self.menu_file.addAction(self.action_exit)
        self.menu_database.addAction(self.action_db_connect)
        self.menu_database.addAction(self.action_db_config)
        self.menu_tools.addAction(self.action_sort)
        self.menu_tools.addAction(self.action_towerrec)
        self.menu_tools.addAction(self.action_export)
        self.menu_help.addAction(self.action_update)
        self.menu_help.addAction(self.action_contact)
        self.menu_help.addAction(self.action_about)
        self.menuBar.addAction(self.menu_file.menuAction())
        self.menuBar.addAction(self.menu_database.menuAction())
        self.menuBar.addAction(self.menu_tools.menuAction())
        self.menuBar.addAction(self.menu_help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_result.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ui_init()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"WindOrder"))
        self.groupBox_farm.setTitle(_translate("MainWindow", "场址风参 *"))
        self.pushButton_farm.setText(_translate("MainWindow", "打开文件"))
        self.groupBox_ref_path.setTitle(_translate("MainWindow", "对比风参"))
        self.label_ref_std.setText(_translate("MainWindow", "标准设计风参："))
        self.pushButton_ref_std.setText(_translate("MainWindow", "打开文件"))
        self.label_ref_cz.setText(_translate("MainWindow", "定制化风参：  "))
        self.pushButton_ref_cz.setText(_translate("MainWindow", "打开文件"))
        self.groupBox_turbine_lib.setTitle(_translate("MainWindow", "机型库"))
        self.groupBox_tower_list.setTitle(_translate("MainWindow", "塔架库"))
        __sortingEnabled = self.listWidget_towers_list.isSortingEnabled()
        self.listWidget_towers_list.setSortingEnabled(False)
        item = self.listWidget_towers_list.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(3)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(4)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(5)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(6)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(7)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(8)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(9)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.listWidget_towers_list.item(10)
        item.setText(_translate("MainWindow", "New Item"))
        self.listWidget_towers_list.setSortingEnabled(__sortingEnabled)
        self.checkBox_select_all.setText(_translate("MainWindow", "全选"))
        self.label_turbine.setText(_translate("MainWindow", "机型："))
        self.label_hubheight.setText(_translate("MainWindow", "塔架类型："))
        self.label_blade.setText(_translate("MainWindow", "叶片："))
        # self.comboBox_custom_key.setText(_translate("MainWindow", "自定义："))
        self.label.setText(_translate("MainWindow", "显示全部："))
        self.checkBox_turbine.setText(_translate("MainWindow", "机型"))
        self.checkBox_blade.setText(_translate("MainWindow", "叶片"))
        self.checkBox_hubheight.setText(_translate("MainWindow", "塔架类型"))
        self.checkBox_custom.setText(_translate("MainWindow", "自定义项"))
        self.pushButton_reset.setText(_translate("MainWindow", "重置"))
        self.groupBox_functools.setTitle(_translate("MainWindow", "功能区"))
        self.pushButton_towerrec.setText(_translate("MainWindow", "推选塔架"))
        self.pushButton_export.setText(_translate("MainWindow", "导出结果"))
        self.pushButton_sort.setText(_translate("MainWindow", "风参排序"))
        self.groupBox_tower_result.setTitle(_translate("MainWindow", "推荐结果"))
        self.tableWidget_tower_result.setSortingEnabled(True)
        self.tabWidget_result.setTabText(self.tabWidget_result.indexOf(self.tab_tower), _translate("MainWindow", "塔架"))
        self.tabWidget_result.setTabText(self.tabWidget_result.indexOf(self.tab_condition), _translate("MainWindow", "Condition"))
        self.tabWidget_result.setTabText(self.tabWidget_result.indexOf(self.tab_m1), _translate("MainWindow", "M=1"))
        self.tabWidget_result.setTabText(self.tabWidget_result.indexOf(self.tab_m10), _translate("MainWindow", "M=10"))
        self.tabWidget_result.setTabText(self.tabWidget_result.indexOf(self.tab_etm), _translate("MainWindow", "ETM"))
        self.menu_file.setTitle(_translate("MainWindow", "文件(&F)"))
        self.menu_database.setTitle(_translate("MainWindow", "数据库(&D)"))
        self.menu_tools.setTitle(_translate("MainWindow", "工具(&T)"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助(&H)"))
        self.action_openfile.setText(_translate("MainWindow", "打开"))
        self.action_deletefile.setText(_translate("MainWindow", "清除"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_db_connect.setText(_translate("MainWindow", "连接"))
        self.action_db_config.setText(_translate("MainWindow", "配置..."))
        self.action_sort.setText(_translate("MainWindow", "风参排序"))
        self.action_towerrec.setText(_translate("MainWindow", "推选塔架"))
        self.action_contact.setText(_translate("MainWindow", "获得帮助"))
        self.action_update.setText(_translate("MainWindow", "检查更新"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_export.setText(_translate("MainWindow", "导出到Excel"))

# import image_rc
    def ui_init(self):
        try:
            with open('./config/config.json', 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, JSONDecodeError) as e:
            config = {}
        state, msg = self.mysql_connect(**config)

        self.groupBox_ref_path.setChecked(False)
        self.groupBox_turbine_lib.setChecked(True)
        self.listWidget_towers_list.clear()
        self.connect()
        # self.read_json()
        self.comboBox_init(state, msg)

    def comboBox_init(self, state, msg):
        if state:
            self.turbine_list = list_upper([''] + sorted(self.tower_sql.query('机组名称')))
            self.blade_list = list_upper([''] + sorted(self.tower_sql.query('叶片名称')))
            self.hubheight_list = list_upper([''] + sorted(self.tower_sql.query('塔架类型')))
            self.custom_key_list = ['自定义项', '塔架段数', '塔架直径', '基础类型', '箱变位置', '归档分类']
            self.custom_value_dict = {k: list_upper([''] + sorted(self.tower_sql.query(k)))
                                      for k in self.custom_key_list}
            self.comboBox_custom_key.clear()
            self.comboBox_custom_value.clear()                            
            self.comboBox_custom_key.addItems(self.custom_key_list)
            custom_key = self.comboBox_custom_key.currentText()
            self.comboBox_custom_value.addItems(self.custom_value_dict[custom_key])
        else:            
            self.statusBar.showMessage(msg, -1)
            self.turbine_list = []
            self.blade_list = []
            self.hubheight_list = []
            self.custom_key_list = []
            self.custom_value_list = []
            self.comboBox_custom_key.clear()
            self.comboBox_custom_value.clear()
            self.comboBox_custom_key.addItems(self.custom_key_list)
            self.comboBox_custom_value.addItems(self.custom_value_list)

        self.comboBox_turbine.clear()
        self.comboBox_blade.clear()
        self.comboBox_hubheight.clear()
        self.comboBox_turbine.addItems(self.turbine_list)
        self.comboBox_blade.addItems(self.blade_list)
        self.comboBox_hubheight.addItems(self.hubheight_list)

    def read_json(self):
        json_folder =  os.path.abspath(os.path.join(THIS_DIR, "./res/Tower_Database/"))
        json_files = os.listdir(json_folder)
        self.db = TowerDataBase()
        for f in json_files:
            full_path = os.path.join(json_folder, f)
            self.db.update(full_path, mode='a')
        
        basic_info = self.db.get_basic_info(self.db.database)
        self.turbine_list = list_upper(['',] + sorted(list(basic_info['turbine_type'])))
        self.comboBox_turbine.addItems(self.turbine_list)
        self.blade_list = list_upper(['',]+ sorted(list(basic_info['blade_type'])))
        self.comboBox_blade.addItems(self.blade_list)
        self.hubheight_list = list_upper(['',]+ sorted(list(basic_info['hub_height'])))
        self.comboBox_hubheight.addItems(self.hubheight_list)
        self.custom_value_list = list_upper(['',]+ sorted(list(basic_info['dev_type'])))
        self.comboBox_custom_value.addItems(self.custom_value_list)

    def connect(self):
        # 文件操作
        self.pushButton_farm.clicked.connect(self.on_pushButton_farm_clicked)
        self.action_openfile.triggered.connect(self.on_pushButton_farm_clicked)
        self.action_deletefile.triggered.connect(self.on_action_deletefile_triggered)
        self.pushButton_ref_std.clicked.connect(self.on_pushButton_ref_std_clicked)
        self.pushButton_ref_cz.clicked.connect(self.on_pushButton_ref_cz_clicked)
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        # 数据库操作
        self.action_db_connect.triggered.connect(self.on_action_db_connect_triggered)
        self.action_db_config.triggered.connect(self.on_action_db_config_triggered)

        # 重置下拉框
        self.pushButton_reset.clicked.connect(self.on_pushButton_reset_clicked)

        # 下拉框选择动作
        self.comboBox_turbine.activated.connect(self.on_comboBox_turbine_activated)
        self.comboBox_blade.activated.connect(self.on_comboBox_blade_activated)
        self.comboBox_hubheight.activated.connect(self.on_comboBox_hubheight_activated)
        self.comboBox_custom_value.activated.connect(self.on_comboBox_custom_value_activated)
        self.comboBox_custom_key.activated.connect(self.on_comboBox_custom_key_activated)

        # 两个group相互抑制
        self.groupBox_ref_path.clicked.connect(self.on_groupBox_ref_path_changChecked)
        self.groupBox_turbine_lib.clicked.connect(self.on_groupBox_turbine_lib_changChecked)

        # 复选框设置下拉框的显示内容
        self.checkBox_turbine.clicked.connect(self.on_checkBox_turbine_clicked)
        self.checkBox_blade.clicked.connect(self.on_checkBox_blade_clicked)
        self.checkBox_hubheight.clicked.connect(self.on_checkBox_hubheight_clicked)
        self.checkBox_custom.clicked.connect(self.on_checkBox_devtype_clicked)

        # 塔架列表数据变化
        self.listWidget_towers_list.currentItemChanged.connect(self.on_listWidget_towers_list_currentItemChanged)

        # 全选
        self.checkBox_select_all.clicked.connect(self.on_checkBox_select_all_clicked)

        # 风参排序
        self.pushButton_sort.clicked.connect(self.on_pushButton_sort_clicked)
        self.action_sort.triggered.connect(self.on_pushButton_sort_clicked)

        # 塔架推选
        self.pushButton_towerrec.clicked.connect(self.on_pushButton_towerrec_clicked)
        self.action_towerrec.triggered.connect(self.on_pushButton_towerrec_clicked)

        # 导出结果
        self.pushButton_export.clicked.connect(self.on_pushButton_export_clicked)
        self.action_export.triggered.connect(self.on_pushButton_export_clicked)

        # 帮助
        self.action_update.triggered.connect(self.update)
        self.action_contact.triggered.connect(self.contact)
        self.action_about.triggered.connect(self.about)

    @staticmethod
    def contact():
        contact_dialog = ContactDialog()
        contact_dialog.exec()

    # @staticmethod
    def about(self):
        about_dialog = aboutDialog(self.version)
        about_dialog.exec()

    def update(self):
        with open('./config/ftp.json', 'r', encoding='utf-8') as f:
            ftp_ = json.load(f)
        self.statusBar.showMessage(f"ftp_host: {ftp_['host']}", 2)
        update_dialog = UpdateDialog(ftp_['host'], self.version)
        update_dialog.exec()

    def mysql_connect(self, **kwargs):
        if kwargs:
            self.tower_sql.set_config(kwargs)
            state, msg = self.tower_sql.connect()
        else:
            state, msg = False, "数据库无法连接，请重新配置！"     

        self.connect_state = state
        self.comboBox_init(state, msg)
        self.statusBar.showMessage(msg, -1)
        return state, msg

    def on_action_db_connect_triggered(self):
        config = {}
        try:
            with open('./config/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            self.statusBar.showMessage('数据库配置信息读取失败！')

        if not config:
            msg = QMessageBox()
            msg.setWindowTitle("警告")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("数据库无法连接，请重新配置！")
            msg.exec()
        else:
            self.mysql_connect(**config)

    def on_action_db_config_triggered(self):
        config_dialog = DBConfigDialog(self.mysql_connect)
        config_dialog.exec()

    def on_groupBox_ref_path_changChecked(self):
        self.groupBox_turbine_lib.setChecked(not self.groupBox_ref_path.isChecked())
    def on_groupBox_turbine_lib_changChecked(self):
        self.groupBox_ref_path.setChecked(not self.groupBox_turbine_lib.isChecked())

    def on_pushButton_farm_clicked(self):
        file_name = QFileDialog.getOpenFileName(None, '选择文件', '', 'Excel Files (*.xls *xlsx)')
        self.statusBar.clearMessage()
        if file_name[0]:
            self.lineEdit_farm.setText(file_name[0])
            self.statusBar.showMessage('风参读取成功')
        else:
            pass
    def on_action_deletefile_triggered(self):
        self.lineEdit_farm.setText("")
        self.lineEdit_ref_std.setText("")
        self.lineEdit_ref_cz.setText("")

    def on_pushButton_ref_std_clicked(self):
        file_name = QFileDialog.getOpenFileName(None, '选择文件', '', 'Excel Files (*.xls *xlsx)')
        self.lineEdit_ref_std.setText(file_name[0])

    def on_pushButton_ref_cz_clicked(self):
        file_name = QFileDialog.getOpenFileName(None, '选择文件', '', 'Excel Files (*.xls *xlsx)')
        self.lineEdit_ref_cz.setText(file_name[0])

    def get_combobox_current_value(self):
        turbine_value = self.comboBox_turbine.currentText()
        hub_value = self.comboBox_hubheight.currentText()
        blade_value = self.comboBox_blade.currentText()
        custom_key = self.comboBox_custom_key.currentText()
        custom_value = self.comboBox_custom_value.currentText()

        value = {'turbine': turbine_value,
                 'hub': hub_value,
                 'blade': blade_value,
                 'custom_key': custom_key,
                 'custom_value': custom_value}
        return value

    def on_listWidget_towers_list_currentItemChanged(self):
        self.selected_towers = []
        self.loads = []

    def on_comboBox_turbine_activated(self):
        combobox_value = self.get_combobox_current_value()

        # filter_inputs = {'叶片名称': combobox_value['blade'],
        #                  '塔架类型': combobox_value['hub'],
        #                  combobox_value['custom_key']: combobox_value['custom_value']}
        # filtered = self.tower_sql.query('机组名称', **filter_inputs)
        # turbine_list = list_upper([''] + sorted(filtered))
        # combobox_update(self.comboBox_turbine, turbine_list, self.checkBox_turbine, self.turbine_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('叶片名称', **filter_inputs)
        blade_list = list_upper(['',]+ sorted(filtered))
        combobox_update(self.comboBox_blade, blade_list, self.checkBox_blade, self.blade_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('塔架类型', **filter_inputs)
        hubheight_list = list_upper(['',]+ sorted(filtered))
        combobox_update(self.comboBox_hubheight, hubheight_list, self.checkBox_hubheight, self.hubheight_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub']}
        filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
        custome_value_list = list_upper(['',]+ sorted(filtered))
        combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
                        self.custom_value_dict[combobox_value['custom_key']])

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        available_tower = sorted(self.tower_sql.query('塔架编号', **filter_inputs))
        listWidget_update(self.listWidget_towers_list, available_tower)

        self.checkBox_select_all.setChecked(False)

    def on_comboBox_blade_activated(self):
        combobox_value = self.get_combobox_current_value()

        filter_inputs = {'叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('机组名称', **filter_inputs)
        turbine_list = list_upper([''] + sorted(filtered))
        combobox_update(self.comboBox_turbine, turbine_list, self.checkBox_turbine, self.turbine_list)

        # filter_inputs = {'机组名称': combobox_value['turbine'],
        #                  '塔架类型': combobox_value['hub'],
        #                  combobox_value['custom_key']: combobox_value['custom_value']}
        # filtered = self.tower_sql.query('叶片名称', **filter_inputs)
        # blade_list = list_upper(['', ] + sorted(filtered))
        # combobox_update(self.comboBox_blade, blade_list, self.checkBox_blade, self.blade_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('塔架类型', **filter_inputs)
        hubheight_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_hubheight, hubheight_list, self.checkBox_hubheight, self.hubheight_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub']}
        filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
        custome_value_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
                        self.custom_value_dict[combobox_value['custom_key']])

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        available_tower = sorted(self.tower_sql.query('塔架编号', **filter_inputs))
        listWidget_update(self.listWidget_towers_list, available_tower)

        self.checkBox_select_all.setChecked(False)

    def on_comboBox_hubheight_activated(self):
        combobox_value = self.get_combobox_current_value()

        filter_inputs = {'叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('机组名称', **filter_inputs)
        turbine_list = list_upper([''] + sorted(filtered))
        combobox_update(self.comboBox_turbine, turbine_list, self.checkBox_turbine, self.turbine_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('叶片名称', **filter_inputs)
        blade_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_blade, blade_list, self.checkBox_blade, self.blade_list)

        # filter_inputs = {'机组名称': combobox_value['turbine'],
        #                  '叶片名称': combobox_value['blade'],
        #                  combobox_value['custom_key']: combobox_value['custom_value']}
        # filtered = self.tower_sql.query('塔架类型', **filter_inputs)
        # hubheight_list = list_upper(['', ] + sorted(filtered))
        # combobox_update(self.comboBox_hubheight, hubheight_list, self.checkBox_hubheight, self.hubheight_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub']}
        filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
        custome_value_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
                        self.custom_value_dict[combobox_value['custom_key']])

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        available_tower = sorted(self.tower_sql.query('塔架编号', **filter_inputs))
        listWidget_update(self.listWidget_towers_list, available_tower)

        self.checkBox_select_all.setChecked(False)

    def on_comboBox_custom_value_activated(self):
        combobox_value = self.get_combobox_current_value()

        filter_inputs = {'叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('机组名称', **filter_inputs)
        turbine_list = list_upper([''] + sorted(filtered))
        combobox_update(self.comboBox_turbine, turbine_list, self.checkBox_turbine, self.turbine_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('叶片名称', **filter_inputs)
        blade_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_blade, blade_list, self.checkBox_blade, self.blade_list)

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        filtered = self.tower_sql.query('塔架类型', **filter_inputs)
        hubheight_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_hubheight, hubheight_list, self.checkBox_hubheight, self.hubheight_list)

        # filter_inputs = {'机组名称': combobox_value['turbine'],
        #                  '叶片名称': combobox_value['blade'],
        #                  '塔架类型': combobox_value['hub']}
        # filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
        # custome_value_list = list_upper(['', ] + sorted(filtered))
        # combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
        #                         self.custom_value_dict[combobox_value['custom_key']])

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        available_tower = sorted(self.tower_sql.query('塔架编号', **filter_inputs))
        listWidget_update(self.listWidget_towers_list, available_tower)

        self.checkBox_select_all.setChecked(False)

    def on_comboBox_custom_key_activated(self):
        combobox_value = self.get_combobox_current_value()

        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub']}
        filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
        custome_value_list = list_upper(['', ] + sorted(filtered))
        combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
                        self.custom_value_dict[combobox_value['custom_key']])

    def on_checkBox_turbine_clicked(self):
        if self.checkBox_turbine.isChecked():
            combobox_update(self.comboBox_turbine, [], self.checkBox_turbine, self.turbine_list)
        else:
            combobox_value = self.get_combobox_current_value()

            filter_inputs = {'叶片名称': combobox_value['blade'],
                             '塔架类型': combobox_value['hub'],
                             combobox_value['custom_key']: combobox_value['custom_value']}
            filtered = self.tower_sql.query('机组名称', **filter_inputs)
            turbine_list = list_upper([''] + sorted(filtered))
            combobox_update(self.comboBox_turbine, turbine_list, self.checkBox_turbine, self.turbine_list)
    
    def on_checkBox_blade_clicked(self):
        if self.checkBox_blade.isChecked():
            combobox_update(self.comboBox_blade, [], self.checkBox_blade, self.blade_list)
        else:
            combobox_value = self.get_combobox_current_value()

            filter_inputs = {'机组名称': combobox_value['turbine'],
                             '塔架类型': combobox_value['hub'],
                             combobox_value['custom_key']: combobox_value['custom_value']}
            filtered = self.tower_sql.query('叶片名称', **filter_inputs)
            blade_list = list_upper(['', ] + sorted(filtered))
            combobox_update(self.comboBox_blade, blade_list, self.checkBox_blade, self.blade_list)

    def on_checkBox_hubheight_clicked(self):
        if self.checkBox_hubheight.isChecked():
            combobox_update(self.comboBox_hubheight, [], self.checkBox_hubheight, self.hubheight_list)
        else:
            combobox_value = self.get_combobox_current_value()

            filter_inputs = {'机组名称': combobox_value['turbine'],
                             '叶片名称': combobox_value['blade'],
                             combobox_value['custom_key']: combobox_value['custom_value']}
            filtered = self.tower_sql.query('塔架类型', **filter_inputs)
            hubheight_list = list_upper(['', ] + sorted(filtered))
            combobox_update(self.comboBox_hubheight, hubheight_list, self.checkBox_hubheight, self.hubheight_list)

    def on_checkBox_devtype_clicked(self):
        if self.checkBox_custom.isChecked():
            custom_key = self.comboBox_custom_key.currentText()
            combobox_update(self.comboBox_custom_value, [], self.checkBox_custom,
                            self.custom_value_dict[custom_key])
        else:
            combobox_value = self.get_combobox_current_value()

            filter_inputs = {'机组名称': combobox_value['turbine'],
                             '叶片名称': combobox_value['blade'],
                             '塔架类型': combobox_value['hub']}
            filtered = self.tower_sql.query(combobox_value['custom_key'], **filter_inputs)
            custome_value_list = list_upper(['', ] + sorted(filtered))
            combobox_update(self.comboBox_custom_value, custome_value_list, self.checkBox_custom,
                            self.custom_value_dict[combobox_value['custom_key']])

    def on_checkBox_select_all_clicked(self):
        if self.checkBox_select_all.isChecked():
            for r in range(self.listWidget_towers_list.count()):
                self.listWidget_towers_list.item(r).setSelected(True)
        else:
            for item in self.listWidget_towers_list.selectedItems():
                row = self.listWidget_towers_list.row(item)
                self.listWidget_towers_list.item(row).setSelected(False)

    def on_pushButton_reset_clicked(self):
        if self.connect_state:
            self.comboBox_turbine.clear()
            self.comboBox_custom_key.clear()
            self.comboBox_custom_value.clear()
            self.comboBox_blade.clear()
            self.comboBox_hubheight.clear()
            self.listWidget_towers_list.clear()
            self.comboBox_turbine.addItems(self.turbine_list)
            self.comboBox_blade.addItems(self.blade_list)
            self.comboBox_hubheight.addItems(self.hubheight_list)
            self.comboBox_custom_key.addItems(self.custom_key_list)
            custom_key = self.comboBox_custom_key.currentText()
            self.comboBox_custom_value.addItems(self.custom_value_dict[custom_key])
            self.checkBox_blade.setChecked(False)
            self.checkBox_custom.setChecked(False)
            self.checkBox_hubheight.setChecked(False)
            self.checkBox_turbine.setChecked(False)
        else:
            self.statusBar.showMessage("数据库未连接")

    def on_pushButton_sort_clicked(self):
        self.statusBar.clearMessage()              
        self.statusBar.showMessage('计算中...')
        wind_path = self.lineEdit_farm.text()
        if wind_path:
            if self.tower_sql.db.is_connected() and self.tower_sql.table_name:
                if self.groupBox_ref_path.isChecked():
                    path_list = []
                    path_list.append((wind_path))
                    this_dir = os.path.dirname(__file__)
                    if self.lineEdit_ref_std.text():
                        path_list.append(self.lineEdit_ref_std.text())
                    if self.lineEdit_ref_cz.text():
                        path_list.append(self.lineEdit_ref_cz.text())
                    res = compare(path_list)
                    plot_widget = PlotWidget(res)
                    plot_widget.plot()
                    plot_widget.show()

                else:
                    selected_towers = [item.text() for item in self.listWidget_towers_list.selectedItems()]

                    # 用于确定选的塔架是否变更, 便于推荐时直接采用载荷结果
                    self.selected_towers = selected_towers

                    ref_wind = self.tower_sql.get_wind_info(selected_towers)

                    res = main_run(wind_path, ref_wind)                    
                    self.loads = res['loads'] if self.selected_towers else {}

                    plot_widget = PlotWidget(res)
                    plot_widget.plot()
                    plot_widget.show()

                    self.statusBar.showMessage('计算完成')
            else:
                if self.groupBox_ref_path.isChecked():
                    path_list = []
                    path_list.append((wind_path))
                    this_dir = os.path.dirname(__file__)
                    if self.lineEdit_ref_std.text():
                        path_list.append(self.lineEdit_ref_std.text())
                    if self.lineEdit_ref_cz.text():
                        path_list.append(self.lineEdit_ref_cz.text())
                    res = compare(path_list)
                    plot_widget = PlotWidget(res)
                    plot_widget.plot()
                    plot_widget.show()
                else:                    
                    res = main_run(wind_path, {})                    
                    self.loads = res['loads'] if self.selected_towers else {}

                    plot_widget = PlotWidget(res)
                    plot_widget.plot()
                    plot_widget.show()

                    self.statusBar.showMessage('计算完成')
        else:
            msg = QMessageBox()
            msg.setWindowTitle("警告")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("缺少场址风参文件！")
            msg.exec()
            self.statusBar.clearMessage()

    def on_pushButton_towerrec_clicked(self):
        self.statusBar.clearMessage()
        self.statusBar.showMessage('计算中...')
        wind_path = self.lineEdit_farm.text()
        if wind_path:
            if self.tower_sql.db.is_connected() and self.tower_sql.table_name:
                selected_towers = [item.text() for item in self.listWidget_towers_list.selectedItems()]
                if self.rec_last_selected_towers == selected_towers:
                    self.clear_result()
                    self.show_result(self.last_available_tower)  # 结果显示
                    self.statusBar.showMessage(f'计算完成，找到{len(self.last_available_tower)}款塔架')
                else:
                    if selected_towers:
                        ref_wind = self.tower_sql.get_wind_info(selected_towers)

                        if self.selected_towers == selected_towers:
                            available_tower = find_available_tower(wind_path, ref_wind, loads=self.loads, sorted_by_weight=False)
                        else:
                            available_tower = find_available_tower(wind_path, ref_wind, loads={}, sorted_by_weight=False)

                        self.rec_last_selected_towers = selected_towers
                        self.last_available_tower = available_tower
                        if available_tower:
                            self.clear_result()
                            self.show_result(available_tower) # 结果显示
                            self.statusBar.showMessage(f'计算完成，找到{len(available_tower)}款塔架')
                        else:
                            self.statusBar.showMessage('未找到合适塔架')
                    else:
                        self.statusBar.showMessage('未选塔架')
            else:
                msg = QMessageBox()
                msg.setWindowTitle("警告")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("数据库未连接！")
                msg.exec()
                self.statusBar.clearMessage()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("警告")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("缺少场址风参文件！")
            msg.exec()     

    def clear_result(self):
        self.tableWidget_tower_result.setRowCount(0)
        self.tableWidget_tower_result.setColumnCount(0)
        self.tableWidget_condition.setRowCount(0)
        self.tableWidget_condition.setColumnCount(0)
        self.tableWidget_m1.setRowCount(0)
        self.tableWidget_m1.setColumnCount(0)
        self.tableWidget_m10.setRowCount(0)
        self.tableWidget_m10.setColumnCount(0)
        self.tableWidget_etm.setRowCount(0)
        self.tableWidget_etm.setColumnCount(0)

    def show_result(self, available_tower):
        bg_brush_blue = QtGui.QBrush(QtGui.QColor(173, 216, 230, 127))  # 浅蓝
        bg_brush_purple = QtGui.QBrush(QtGui.QColor(230, 230, 250, 127))  # 浅紫

        # 塔架 tab
        tower_count = len(available_tower)
        self.tableWidget_tower_result.setRowCount(tower_count)  
        self.tableWidget_tower_result.setColumnCount(7)

        item_tower_id = QtWidgets.QTableWidgetItem('塔架编号')
        self.tableWidget_tower_result.setHorizontalHeaderItem(0, item_tower_id)

        item_tower_limit = QtWidgets.QTableWidgetItem('塔架受限')
        self.tableWidget_tower_result.setHorizontalHeaderItem(1, item_tower_limit)

        item_ul_prop = QtWidgets.QTableWidgetItem('极限比例')
        self.tableWidget_tower_result.setHorizontalHeaderItem(2, item_ul_prop)

        item_fl_prop = QtWidgets.QTableWidgetItem('疲劳比例')
        self.tableWidget_tower_result.setHorizontalHeaderItem(3, item_fl_prop)

        item_wind_limit = QtWidgets.QTableWidgetItem('风载属性')
        self.tableWidget_tower_result.setHorizontalHeaderItem(4, item_wind_limit)

        item_tower_weight = QtWidgets.QTableWidgetItem('塔架重量(t)')
        self.tableWidget_tower_result.setHorizontalHeaderItem(5, item_tower_weight)

        item_std_spec = QtWidgets.QTableWidgetItem('塔筒屈曲标准')
        self.tableWidget_tower_result.setHorizontalHeaderItem(6, item_std_spec)

        # condition tab
        self.tableWidget_condition.setRowCount(tower_count)
        self.tableWidget_condition.setColumnCount(8)

        item_tower_id_copy = QtWidgets.QTableWidgetItem('塔架编号')
        self.tableWidget_condition.setHorizontalHeaderItem(0, item_tower_id_copy)

        item_air_density = QtWidgets.QTableWidgetItem('ρ')
        self.tableWidget_condition.setHorizontalHeaderItem(1, item_air_density)

        item_wind_vave = QtWidgets.QTableWidgetItem('Vave')
        self.tableWidget_condition.setHorizontalHeaderItem(2, item_wind_vave)

        item_weibull_a = QtWidgets.QTableWidgetItem('A')
        self.tableWidget_condition.setHorizontalHeaderItem(3, item_weibull_a)

        item_weibull_k = QtWidgets.QTableWidgetItem('K')
        self.tableWidget_condition.setHorizontalHeaderItem(4, item_weibull_k)

        item_wind_shear = QtWidgets.QTableWidgetItem('α')
        self.tableWidget_condition.setHorizontalHeaderItem(5, item_wind_shear)

        item_inflow = QtWidgets.QTableWidgetItem('θmean')
        self.tableWidget_condition.setHorizontalHeaderItem(6, item_inflow)

        item_wind_v50 = QtWidgets.QTableWidgetItem('V50')
        self.tableWidget_condition.setHorizontalHeaderItem(7, item_wind_v50)

        self.tableWidget_m1.setColumnCount(tower_count*2)
        self.tableWidget_m10.setColumnCount(tower_count*2)
        self.tableWidget_etm.setColumnCount(tower_count*2)            
        
        # filtered = self.db.filter(**filter_inputs)
        # filtered_wind = self.db.get_wind_info(filtered)

        combobox_value = self.get_combobox_current_value()
        filter_inputs = {'机组名称': combobox_value['turbine'],
                         '叶片名称': combobox_value['blade'],
                         '塔架类型': combobox_value['hub'],
                         combobox_value['custom_key']: combobox_value['custom_value']}
        
        tower_list = self.tower_sql.query('塔架编号', **filter_inputs)
        filtered_wind = self.tower_sql.get_wind_info(tower_list)
        
        self.wind_info = filtered_wind
        self.tower_info = available_tower

        rows = []
        for tower_id, tower in available_tower.items():
            labels = list(available_tower.keys())
            i = labels.index(tower_id)

            # 塔架, 第一个tab
            item_id = QtWidgets.QTableWidgetItem()
            item_id.setText(tower_id)
            if tower['wind_limit'] == 'A':
                item_id.setFont(QtGui.QFont('微软雅黑', 10, QtGui.QFont.Bold))
            item_id.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_id.setBackground(bg_brush_purple)

            item_tower_limit = QtWidgets.QTableWidgetItem()
            item_tower_limit.setText(str(tower['tower_limit']))
            item_tower_limit.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_tower_limit.setBackground(bg_brush_blue)

            item_ul_prop = QtWidgets.QTableWidgetItem()
            item_ul_prop.setText(str(tower['ul_prop']))
            item_ul_prop.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_ul_prop.setBackground(bg_brush_purple)

            item_fl_prop = QtWidgets.QTableWidgetItem()
            item_fl_prop.setText(str(tower['fl_prop']))
            item_fl_prop.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_fl_prop.setBackground(bg_brush_blue)

            item_wind_limit = QtWidgets.QTableWidgetItem()
            item_wind_limit.setText(str(tower['wind_limit']))
            item_wind_limit.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_wind_limit.setBackground(bg_brush_purple)

            item_weight = QtWidgets.QTableWidgetItem()
            item_weight.setText(str(tower['weight']))
            item_weight.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_weight.setBackground(bg_brush_blue)

            item_std_spec = QtWidgets.QTableWidgetItem()
            item_std_spec.setText(str(tower['std_spec']))
            item_std_spec.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_std_spec.setBackground(bg_brush_purple)

            # condition tab
            item_id_copy = QtWidgets.QTableWidgetItem()
            item_id_copy.setText(tower_id)
            item_id_copy.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_id_copy.setBackground(bg_brush_purple)

            item_air_density = QtWidgets.QTableWidgetItem()
            item_air_density.setText(str(filtered_wind[tower_id]['condition']['ρ'][tower_id]))
            item_air_density.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_air_density.setBackground(bg_brush_blue)

            item_wind_vave = QtWidgets.QTableWidgetItem()
            item_wind_vave.setText(str(filtered_wind[tower_id]['condition']['vave'][tower_id]))
            item_wind_vave.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_wind_vave.setBackground(bg_brush_purple)

            item_weibull_a = QtWidgets.QTableWidgetItem()
            item_weibull_a.setText(str(round(filtered_wind[tower_id]['condition']['a'][tower_id], 2)))
            item_weibull_a.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_weibull_a.setBackground(bg_brush_blue)

            item_weibull_k = QtWidgets.QTableWidgetItem()
            item_weibull_k.setText(str(round(filtered_wind[tower_id]['condition']['k'][tower_id], 2)))
            item_weibull_k.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_weibull_k.setBackground(bg_brush_purple)

            item_wind_shear = QtWidgets.QTableWidgetItem()
            item_wind_shear.setText(str(filtered_wind[tower_id]['condition']['α'][tower_id]))
            item_wind_shear.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_wind_shear.setBackground(bg_brush_blue)

            item_inflow = QtWidgets.QTableWidgetItem()
            item_inflow.setText(str(filtered_wind[tower_id]['condition']['θmean'][tower_id]))
            item_inflow.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_inflow.setBackground(bg_brush_purple)

            item_wind_v50 = QtWidgets.QTableWidgetItem()
            item_wind_v50.setText(str(round(filtered_wind[tower_id]['condition']['v50'][tower_id], 2)))
            item_wind_v50.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_wind_v50.setBackground(bg_brush_blue)

            self.tableWidget_tower_result.setItem(i, 0, item_id)
            self.tableWidget_tower_result.setItem(i, 1, item_tower_limit)
            self.tableWidget_tower_result.setItem(i, 2, item_ul_prop)
            self.tableWidget_tower_result.setItem(i, 3, item_fl_prop)
            self.tableWidget_tower_result.setItem(i, 4, item_wind_limit)
            self.tableWidget_tower_result.setItem(i, 5, item_weight)
            self.tableWidget_tower_result.setItem(i, 6, item_std_spec)

            self.tableWidget_condition.setItem(i, 0, item_id_copy)
            self.tableWidget_condition.setItem(i, 1, item_air_density)
            self.tableWidget_condition.setItem(i, 2, item_wind_vave)
            self.tableWidget_condition.setItem(i, 3, item_weibull_a)
            self.tableWidget_condition.setItem(i, 4, item_weibull_k)
            self.tableWidget_condition.setItem(i, 5, item_wind_shear)
            self.tableWidget_condition.setItem(i, 6, item_inflow)
            self.tableWidget_condition.setItem(i, 7, item_wind_v50)

            # 湍流表行表头
            self.tableWidget_m1.setHorizontalHeaderItem(2*i, QtWidgets.QTableWidgetItem('WindSpeed'))
            self.tableWidget_m1.setHorizontalHeaderItem(2*i + 1, QtWidgets.QTableWidgetItem(tower_id))
            self.tableWidget_m10.setHorizontalHeaderItem(2*i, QtWidgets.QTableWidgetItem('WindSpeed'))
            self.tableWidget_m10.setHorizontalHeaderItem(2*i + 1, QtWidgets.QTableWidgetItem(tower_id))
            self.tableWidget_etm.setHorizontalHeaderItem(2*i, QtWidgets.QTableWidgetItem('WindSpeed'))
            self.tableWidget_etm.setHorizontalHeaderItem(2*i + 1, QtWidgets.QTableWidgetItem(tower_id))

            # 湍流表列
            fill_ti_partial = partial(self.fill_ti, i, tower_id, rows, filtered_wind, bg_brush_blue, bg_brush_purple)
            fill_ti_partial(self.tableWidget_m1, 'm1')
            fill_ti_partial(self.tableWidget_m10, 'm10')
            fill_ti_partial(self.tableWidget_etm, 'etm')

    # 填充湍流数据
    @staticmethod
    def fill_ti(i, tower_id, rows, filtered_wind, bg_brush_blue, bg_brush_purple, table, type):
        wind_speed = filtered_wind[tower_id][type]['Wind Speed']
        ti = filtered_wind[tower_id][type][tower_id]
        rows.append(len(ti))

        table.setRowCount(max(rows))
        for j in range(len(ti)):
            item_wind_speed = QtWidgets.QTableWidgetItem(str(wind_speed[j]))
            item_wind_speed.setBackground(bg_brush_purple)
            item_wind_speed.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_wind_speed.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            table.setItem(j, 2*i, item_wind_speed)            
            item_ti = QtWidgets.QTableWidgetItem(str(ti[j]))
            item_ti.setBackground(bg_brush_blue)
            item_ti.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item_ti.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            table.setItem(j, 2*i+1, item_ti)
    
    def on_pushButton_export_clicked(self):
        if not self.wind_info or not self.tower_info:
            msg = QMessageBox()
            msg.setWindowTitle("警告")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("没有结果，请先进行塔架推荐。")
            msg.exec()  
        else:
            wind_path = self.lineEdit_farm.text()
            if os.path.splitext(wind_path)[-1] == '.xls':
                msg = QMessageBox()
                msg.setWindowTitle("警告")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("该功能暂不支持.xls格式的风参，\n可手动转换成.xlsx格式再执行。")
                msg.exec()  
            else:
                wind_folder = os.path.split(wind_path)[0]
                excel = ExcelAPI(wind_path)
                excel.update(self.wind_info, self.tower_info)

                savefile = QFileDialog.getSaveFileName(None, '保存文件', wind_folder, 'Excel Files (*xlsx)')
                filename = savefile[0] + '.xlsx'        
                excel.write(filename)


class DBConfigDialog(QtWidgets.QDialog):
    def __init__(self, func_mysql_connect):
        super().__init__()

        self.func_mysql_connect = func_mysql_connect
        self.ui_show()

    def ui_show(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('数据库配置')
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./config_act.png")), QtGui.QIcon.Normal,
                              QtGui.QIcon.Off)
        self.setWindowIcon(window_icon)
        self.setFixedHeight(240)
        self.setMaximumWidth(400)

        layout = QtWidgets.QVBoxLayout(self)
        self.grid_layout = QtWidgets.QGridLayout()
        labels = ['数据库名称:', '表名称:', '', '主机:', '端口:', '用户:', '密码:']
        try:
            with open('./config/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (FileNotFoundError, JSONDecodeError) as e:
            config = {}
        if config:
            auto_filling = config
            auto_filling[''] = ''
        else:
            auto_filling = {'数据库名称:': '', '表名称:': '', '主机:': '', '':'',
                            '端口:': '3306', '用户:': '', '密码:': ''}
        for i, label in enumerate(labels):
            lbl = QtWidgets.QLabel(label)
            self.grid_layout.addWidget(lbl, i, 0)
            if label:
                line_edit = QtWidgets.QLineEdit(auto_filling[label])
                if label == '密码:':
                    line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
                self.grid_layout.addWidget(line_edit, i, 1)
            else:
                self.grid_layout.addWidget(lbl, i, 1)
        #
        group = QtWidgets.QGroupBox()
        group.resize(270, 355)
        group.setStyleSheet('background: white')
        group.setLayout(self.grid_layout)

        hbox_layout = QtWidgets.QHBoxLayout(self)
        self.set_default_check = QtWidgets.QCheckBox('设为默认', self)
        self.set_default_check.move(15, 360)
        connect_btn = QtWidgets.QPushButton('连接', self)
        connect_btn.move(100, 360)
        cancel_btn = QtWidgets.QPushButton('取消', self)
        cancel_btn.move(200, 360)

        connect_btn.clicked.connect(self.on_connect_btn_clicked)
        cancel_btn.clicked.connect(self.close)

        spacer1 = QtWidgets.QSpacerItem(80, 20)
        hbox_layout.addWidget(self.set_default_check)
        hbox_layout.addSpacerItem(spacer1)
        hbox_layout.addWidget(connect_btn)
        hbox_layout.addWidget(cancel_btn)

        layout.addWidget(group)
        layout.addLayout(hbox_layout)
        self.setLayout(layout)

        self.show()

    def on_connect_btn_clicked(self):
        config = {'数据库名称:': self.grid_layout.itemAtPosition(0, 1).widget().text(),
                  '表名称:': self.grid_layout.itemAtPosition(1, 1).widget().text(),
                  '主机:': self.grid_layout.itemAtPosition(3, 1).widget().text(),
                  '端口:': self.grid_layout.itemAtPosition(4, 1).widget().text(),
                  '用户:': self.grid_layout.itemAtPosition(5, 1).widget().text(),
                  '密码:': self.grid_layout.itemAtPosition(6, 1).widget().text()}
        self.func_mysql_connect(**config)
        if self.set_default_check.isChecked():
            with open('./config/config.json', 'w', encoding='UTF-8') as f:
                json.dump(config, f)
        self.close()


class UpdateDialog(QtWidgets.QDialog):
    def __init__(self, host, version):
        super().__init__()
        self.host = host
        self.current_version = version
        self.label_img = QtWidgets.QLabel(self)
        self.label_txt = QtWidgets.QLabel(self)
        self.download_btn = QtWidgets.QPushButton('下载新版本', self)
        self.cancel_btn = QtWidgets.QPushButton('取消', self)
        self.ftp = MyFTP(self.host)
        self.new_version_name = ''

        self.ui_show()
        self.update_checking()

    def ui_show(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('检查更新')
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./update.png")), QtGui.QIcon.Normal,
                              QtGui.QIcon.Off)
        self.setWindowIcon(window_icon)
        self.setFixedHeight(240)
        self.setFixedWidth(300)

        group = QtWidgets.QGroupBox(self)
        vlayout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        self.label_img.setStyleSheet("border-image:url('./res/img/find.png')")
        self.label_img.setFixedHeight(60)
        self.label_img.setFixedWidth(60)
        hlayout.addWidget(self.label_img, alignment=QtCore.Qt.AlignCenter)

        self.label_txt.setText('正在检查更新...')
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.label_txt, alignment=QtCore.Qt.AlignCenter)
        group.setLayout(vlayout)
        group.setStyleSheet('border: none')
        group.resize(260, 100)
        group.move(20, 40)

        self.download_btn.setEnabled(False)
        self.download_btn.resize(130, 25)
        self.download_btn.move(15, 200)
        self.cancel_btn.resize(130, 25)
        self.cancel_btn.move(155, 200)

        self.download_btn.clicked.connect(self.on_download_btn_clicked)
        self.cancel_btn.clicked.connect(self.canceled)

        self.show()

    def update_checking(self):
        check_result = self.ftp.check_update(self.current_version)
        if check_result[0]:
            self.new_version_name = check_result[1]
            new_version_no = self.new_version_name[11:]
            self.label_img.setStyleSheet("border-image:url('./res/img/file.png')")
            self.label_txt.setText(f'可更新至{new_version_no}版')
            self.download_btn.setEnabled(True)
        else:
            self.label_img.setStyleSheet("border-image:url('./res/img/warning.png')")
            self.label_txt.setText(check_result[1])

    def canceled(self):
        self.close()

    def on_download_btn_clicked(self):
        save_file = QFileDialog.getSaveFileName(None, '保存文件', self.new_version_name, 'Zip File (*zip)')
        local_file_path = save_file[0] + '.zip'
        remote_file_path = os.path.join('/', self.new_version_name, self.new_version_name + '.zip')
        self.ftp.download(local_file_path, remote_file_path)
        self.close()


class ContactDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.ui_show()

    def ui_show(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('获得帮助')
        icon_contact = QtGui.QIcon()
        icon_contact.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./help.png")),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon_contact)
        self.resize(320, 260)
        label1 = QtWidgets.QLabel(self)
        label1.setText("软件使用过程中有任何疑问，请联系以下人员：")
        label1.setFont(QtGui.QFont("微软雅黑", 10, QtGui.QFont.Bold))
        label2 = QtWidgets.QLabel(self)
        label2.setOpenExternalLinks(True)
        label2.setText("<a href=\"http://mail.goldwind.com.cn\">wangshiwen@goldwind.com.cn")
        label2.setFont(QtGui.QFont("微软雅黑", 10))
        label3 = QtWidgets.QLabel(self)
        label3.setOpenExternalLinks(True)
        label3.setText("<a href=\"http://mail.goldwind.com.cn\">liuhu@goldwind.com.cn")
        label3.setFont(QtGui.QFont("微软雅黑", 10))

        spacer_top = QtWidgets.QSpacerItem(20, 40)
        spacer_bottom = QtWidgets.QSpacerItem(20, 100)
        spacer_left = QtWidgets.QSpacerItem(20, 100)
        spacer_right = QtWidgets.QSpacerItem(0, 100)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addSpacerItem(spacer_top)
        vlayout.addWidget(label1)
        vlayout.addWidget(label3)
        vlayout.addWidget(label2)
        vlayout.addSpacerItem(spacer_bottom)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addSpacerItem(spacer_left)
        layout.addLayout(vlayout)
        layout.addSpacerItem(spacer_right)

        self.setLayout(layout)

        self.show()


class aboutDialog(QtWidgets.QDialog):
    def __init__(self, version):
        self.version = version
        super().__init__()

        self.ui_show()

    def ui_show(self):
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('关于')
        icon_about = QtGui.QIcon()
        icon_about.addPixmap(QtGui.QPixmap(os.path.join(IMG_PATH, "./about.png")), QtGui.QIcon.Normal,
                             QtGui.QIcon.Off)
        self.setWindowIcon(icon_about)
        self.resize(320, 260)

        label1 = QtWidgets.QLabel(self)
        label1.setStyleSheet("border-image:url('./res/img/sort_ico.png')")
        label1.setFixedHeight(45)
        label1.setFixedWidth(45)

        label2 = QtWidgets.QLabel(self)
        label2.setText("WindOrder")
        label2.setFont(QtGui.QFont("微软雅黑", 18, QtGui.QFont.Bold))
        label2.setStyleSheet("color: blue")

        label3 = QtWidgets.QLabel(self)
        label3.setText(f'Version: {self.version}')
        label4 = QtWidgets.QLabel(self)
        label4.setText('Data: 2019-08-26 19:31:56')
        label5 = QtWidgets.QLabel(self)
        label5.setText('OS: Windows-10-10.0.18362-SP0')

        layout1 = QtWidgets.QVBoxLayout()
        spacer_top = QtWidgets.QSpacerItem(20, 20)
        layout1.addSpacerItem(spacer_top)
        layout1.addWidget(label2)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(label1)
        layout2.addLayout(layout1)

        layout3 = QtWidgets.QVBoxLayout()
        layout3.addWidget(label3)
        layout3.addWidget(label4)
        layout3.addWidget(label5)

        spacer_med = QtWidgets.QSpacerItem(20, 100)
        spacer_btm = QtWidgets.QSpacerItem(20, 20)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(layout2)
        layout.addSpacerItem(spacer_med)
        layout.addLayout(layout3)
        layout.addSpacerItem(spacer_btm)

        self.setLayout(layout)

        self.show()


class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kw):
        super(MyLineEdit, self).__init__(*args)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(MyLineEdit, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(MyLineEdit, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.setText(url.toLocalFile())
            event.acceptProposedAction()
        else:
            super(MyLineEdit, self).dropEvent(event)
