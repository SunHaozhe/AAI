#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Sun Jun 25 2017

@author: Haozhe Sun
"""

from gui import *
from PyQt5.QtCore import QStringListModel, QAbstractTableModel, Qt, QAbstractTableModel

class RsModel(QAbstractTableModel):

    def __init__(self,data1 = [[]],headers =[],parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.__data1=data1
        self._headers=headers

    def rowCount(self, parent):
        return len(data1)

    def columnCount(self, parent):
        return len(data1[0])

    def data(self, index, role):
        if role == Qt.ToolTipRole:
            row = index.row
            return "Crédit"
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__data1[row][column]
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__data1[row][column]
            return value

    def flags(self, index):
        return Qt.ItemIsEnabled | (Qt.ItemIsEditable) | Qt.ItemIsSelectable


#logical links
data0 = ["2", "g", "3"] # An example
llModel = QStringListModel(data0)

#Reality status
data1 = [["The door is repainted","True"], ["The door is wrecked", "False"], ["The door is beautiful", "True"]] # An example
rsModel = RsModel(data1)

