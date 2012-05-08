# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ants.ui'
#
# Created: Tue May  8 15:17:08 2012
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
        MainWindow.resize(653, 472)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "AntPop", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.arena = QtGui.QLabel(self.centralwidget)
        self.arena.setGeometry(QtCore.QRect(10, 10, 481, 451))
        self.arena.setMinimumSize(QtCore.QSize(320, 240))
        self.arena.setFrameShape(QtGui.QFrame.Box)
        self.arena.setText(_fromUtf8(""))
        self.arena.setObjectName(_fromUtf8("arena"))
        self.initialEnergy = QtGui.QLineEdit(self.centralwidget)
        self.initialEnergy.setGeometry(QtCore.QRect(500, 30, 112, 26))
        self.initialEnergy.setInputMask(_fromUtf8(""))
        self.initialEnergy.setText(QtGui.QApplication.translate("MainWindow", "280", None, QtGui.QApplication.UnicodeUTF8))
        self.initialEnergy.setObjectName(_fromUtf8("initialEnergy"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(499, 11, 81, 16))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Initial Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.foodEnergy = QtGui.QLineEdit(self.centralwidget)
        self.foodEnergy.setGeometry(QtCore.QRect(500, 150, 112, 26))
        self.foodEnergy.setInputMask(_fromUtf8(""))
        self.foodEnergy.setText(QtGui.QApplication.translate("MainWindow", "18", None, QtGui.QApplication.UnicodeUTF8))
        self.foodEnergy.setObjectName(_fromUtf8("foodEnergy"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 130, 72, 16))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Food Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.breedEnergy = QtGui.QLineEdit(self.centralwidget)
        self.breedEnergy.setGeometry(QtCore.QRect(500, 270, 112, 26))
        self.breedEnergy.setInputMask(_fromUtf8(""))
        self.breedEnergy.setText(QtGui.QApplication.translate("MainWindow", "600", None, QtGui.QApplication.UnicodeUTF8))
        self.breedEnergy.setObjectName(_fromUtf8("breedEnergy"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(500, 250, 78, 16))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Breed Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.maxEnergy = QtGui.QLineEdit(self.centralwidget)
        self.maxEnergy.setGeometry(QtCore.QRect(500, 80, 112, 26))
        self.maxEnergy.setInputMask(_fromUtf8(""))
        self.maxEnergy.setText(QtGui.QApplication.translate("MainWindow", "900", None, QtGui.QApplication.UnicodeUTF8))
        self.maxEnergy.setObjectName(_fromUtf8("maxEnergy"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(500, 60, 106, 16))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Maximum Energy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.initFood = QtGui.QLineEdit(self.centralwidget)
        self.initFood.setGeometry(QtCore.QRect(500, 200, 112, 26))
        self.initFood.setInputMask(_fromUtf8(""))
        self.initFood.setText(QtGui.QApplication.translate("MainWindow", "800", None, QtGui.QApplication.UnicodeUTF8))
        self.initFood.setObjectName(_fromUtf8("initFood"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(500, 180, 97, 16))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Inital Food Level", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.reset = QtGui.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(499, 423, 85, 27))
        self.reset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.reset.setObjectName(_fromUtf8("reset"))
        self.restart = QtGui.QPushButton(self.centralwidget)
        self.restart.setGeometry(QtCore.QRect(500, 390, 85, 27))
        self.restart.setText(QtGui.QApplication.translate("MainWindow", "Start/Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.restart.setObjectName(_fromUtf8("restart"))
        self.GluttonyKills = QtGui.QCheckBox(self.centralwidget)
        self.GluttonyKills.setGeometry(QtCore.QRect(500, 110, 111, 21))
        self.GluttonyKills.setText(QtGui.QApplication.translate("MainWindow", "Gluttony Kills", None, QtGui.QApplication.UnicodeUTF8))
        self.GluttonyKills.setObjectName(_fromUtf8("GluttonyKills"))
        self.Mutations = QtGui.QCheckBox(self.centralwidget)
        self.Mutations.setGeometry(QtCore.QRect(500, 300, 101, 21))
        self.Mutations.setText(QtGui.QApplication.translate("MainWindow", "Mutations", None, QtGui.QApplication.UnicodeUTF8))
        self.Mutations.setObjectName(_fromUtf8("Mutations"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.initialEnergy, self.maxEnergy)
        MainWindow.setTabOrder(self.maxEnergy, self.GluttonyKills)
        MainWindow.setTabOrder(self.GluttonyKills, self.foodEnergy)
        MainWindow.setTabOrder(self.foodEnergy, self.initFood)
        MainWindow.setTabOrder(self.initFood, self.breedEnergy)
        MainWindow.setTabOrder(self.breedEnergy, self.Mutations)
        MainWindow.setTabOrder(self.Mutations, self.restart)
        MainWindow.setTabOrder(self.restart, self.reset)

    def retranslateUi(self, MainWindow):
        pass

