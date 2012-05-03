# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ants.ui'
#
# Created: Thu May  3 15:16:57 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(645, 409)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "AntPop", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.arena = QtGui.QLabel(self.centralwidget)
        self.arena.setGeometry(QtCore.QRect(10, 10, 481, 391))
        self.arena.setMinimumSize(QtCore.QSize(320, 240))
        self.arena.setFrameShape(QtGui.QFrame.Box)
        self.arena.setText(_fromUtf8(""))
        self.arena.setObjectName(_fromUtf8("arena"))
        self.initialEnergy = QtGui.QLineEdit(self.centralwidget)
        self.initialEnergy.setGeometry(QtCore.QRect(502, 60, 141, 23))
        self.initialEnergy.setInputMask(_fromUtf8(""))
        self.initialEnergy.setText(QtGui.QApplication.translate("MainWindow", "280", None, QtGui.QApplication.UnicodeUTF8))
        self.initialEnergy.setObjectName(_fromUtf8("initialEnergy"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(500, 40, 141, 16))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Initial Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.foodEnergy = QtGui.QLineEdit(self.centralwidget)
        self.foodEnergy.setGeometry(QtCore.QRect(502, 210, 141, 23))
        self.foodEnergy.setInputMask(_fromUtf8(""))
        self.foodEnergy.setText(QtGui.QApplication.translate("MainWindow", "18", None, QtGui.QApplication.UnicodeUTF8))
        self.foodEnergy.setObjectName(_fromUtf8("foodEnergy"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 190, 141, 16))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Food Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.breedEnergy = QtGui.QLineEdit(self.centralwidget)
        self.breedEnergy.setGeometry(QtCore.QRect(502, 160, 141, 23))
        self.breedEnergy.setInputMask(_fromUtf8(""))
        self.breedEnergy.setText(QtGui.QApplication.translate("MainWindow", "600", None, QtGui.QApplication.UnicodeUTF8))
        self.breedEnergy.setObjectName(_fromUtf8("breedEnergy"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(500, 140, 141, 16))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Breed Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.maxEnergy = QtGui.QLineEdit(self.centralwidget)
        self.maxEnergy.setGeometry(QtCore.QRect(500, 110, 141, 23))
        self.maxEnergy.setInputMask(_fromUtf8(""))
        self.maxEnergy.setText(QtGui.QApplication.translate("MainWindow", "900", None, QtGui.QApplication.UnicodeUTF8))
        self.maxEnergy.setObjectName(_fromUtf8("maxEnergy"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(498, 90, 141, 16))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Maximum Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.initFood = QtGui.QLineEdit(self.centralwidget)
        self.initFood.setGeometry(QtCore.QRect(502, 260, 141, 23))
        self.initFood.setInputMask(_fromUtf8(""))
        self.initFood.setText(QtGui.QApplication.translate("MainWindow", "800", None, QtGui.QApplication.UnicodeUTF8))
        self.initFood.setObjectName(_fromUtf8("initFood"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(500, 240, 141, 16))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Inital Food Level", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.reset = QtGui.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(530, 350, 81, 27))
        self.reset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.reset.setObjectName(_fromUtf8("reset"))
        self.restart = QtGui.QPushButton(self.centralwidget)
        self.restart.setGeometry(QtCore.QRect(530, 310, 81, 27))
        self.restart.setText(QtGui.QApplication.translate("MainWindow", "Start/Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.restart.setObjectName(_fromUtf8("restart"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

