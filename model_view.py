#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Sunday Jun 25 2017

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
        return len(self.__data1)

    def columnCount(self, parent):
        return len(self.__data1[0])

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

"""    
def newElementListView(NewStringElement):
    rowcount = llModel.rowCount()
    modelindex = llModel.index(rowcount)
    llModel.setData(modelindex, NewStringElement)
    
def newElementTableView(NewStringElement):
    rowcount1 = rsModel.rowCount()
    modelindex1 = rsModel.index(rowcount1)
    rsModel.setData(modelindex1, NewStringElement)
"""

#logical links
dataLogicalLinks = ["nice_surface <=== burn_off + -wood_wrecked", "nice_surface <=== sanding + -several_layers + -wood_wrecked",
         "nice_surface <=== filler_compound + -wood_wrecked","nice_doors <=== repaint + nice_surface",
         "tough_work <=== burn_off + mouldings + -wire_brush",
         "wood_wrecked <=== wire_brush + soft_wood",
         "-nice_surface <=== wood_wrecked"] # An example
llModel = QStringListModel(dataLogicalLinks)

#Reality status
dataRealityStatus = [["The door is repainted","True"], ["The door is wrecked", "False"], ["The door is beautiful", "True"]] # An example
rsModel = RsModel(dataRealityStatus)

