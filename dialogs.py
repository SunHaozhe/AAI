#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Mon Jun 26 2017

@author: Haozhe Sun
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPixmap

class Help_Dialog1(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 250)

        strMessage = "Tap space to continue !"
        self.dialoglabel = QtWidgets.QLabel(Dialog)
        self.dialoglabel.setText(strMessage)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Help", "Help"))

class Help_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 250)

        self.dialoglabel = QtWidgets.QLabel(Dialog)
        pixmap = QPixmap("resources.png")
        self.dialoglabel.setPixmap(pixmap)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Help", "Help"))