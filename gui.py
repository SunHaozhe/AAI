#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Thursday Jun 22 2017

@author: Haozhe Sun
"""

import sys
from PyQt5.QtWidgets import (QPushButton, QApplication, QMessageBox, QDesktopWidget,
                            QToolTip, QMainWindow,QAction, qApp, QTextEdit, QGridLayout,
                             QLabel, QLineEdit, QWidget, QHBoxLayout, QComboBox, QFrame,
                             QGroupBox, QListWidget, QTableWidget, QListView, QTableView,
                             QAbstractItemView, QDialog, QVBoxLayout)
from PyQt5.QtCore import QCoreApplication, QSize, QMetaObject
from PyQt5.QtCore import QStringListModel, QAbstractTableModel, Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont
from dialogs import *
from random import randint
from preprocessing import Preprocessor
from themes import *


class MainWindow(QMainWindow):
    """To define the main window of our program"""

    def __init__(self):
        super().__init__()

        self.editIsVisible = False
        self.inputString = ""
        self.themeNames = ("Doors", "Tennis", "Proportional")
        self.themeNameDict = {self.themeNames[0]: 0, self.themeNames[1]: 1, self.themeNames[2]: 2}
        self.theme = Theme(self.themeNames[0])
        self.themeIterator = None
        self.llModel = None
        self.rsModel = None

        self.__initUI()

    def __initUI(self):
        """To initialize the main window"""

        #To set up a status bar
        self.statusBar()

        #To set up a menu bar
        self.__initMenuBar()

        #To set up the main layout
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.__setupGridLayout())

        #To set up size, position and title of the main window
        sizeTuple = (1200, 600)
        self.resize(*sizeTuple)
        self.setMaximumSize(*sizeTuple)
        self.setMinimumSize(*sizeTuple)
        self.__center()
        self.setWindowTitle('Argumentator_')

        #We can add an icon if we need
        #self.setWindowIcon(QIcon('XXX.png'))

        self.__updateTheme()

        self.show()


    def __initMenuBar(self):
        pass
        """exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # This command is for Mac OS
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)"""

    def closeEvent(self, event):
        """To reimplement the behavior when we click on the X button."""
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def __center(self):
        """To center the program main window"""
        rectangle_position = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle_position.moveCenter(center_point)
        self.move(rectangle_position.topLeft())

    def __setupGridLayout(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        self.theme_label = QLabel("                                     Theme :",self)
        self.combo_box = QComboBox(self)
        self.__initComboBox()
        self.begin_button = QPushButton("Begin",self)
        self.continue_button = QPushButton("Continue",self)
        self.reset_button = QPushButton("Reset",self)
        self.help_button  = QPushButton("Help", self)

        self.combo_box.setStatusTip("Please choose a argumenting theme.")
        self.begin_button.setStatusTip("Tap to begin the argumentator procedure.")
        self.continue_button.setStatusTip("Tap to continue argumenting.")
        self.reset_button.setStatusTip(("Tap to reset all program."))
        self.help_button.setStatusTip("Tap to see the help.")

        self.reality_status_label   = QLabel("Reality status :",self)
        self.console_label          = QLabel("Console :", self)
        self.logical_links_label    = QLabel("Logical links :",self)
        self.reality_status    = QTableView(self)
        self.console           = QTextEdit()
        self.logical_links     = QListView(self)
        self.console.setReadOnly(True)

        self.reality_status.setStatusTip('The reality status of the "world".')
        self.console.setStatusTip("The state of the argumenting procedure.")
        self.logical_links.setStatusTip('The logical links between different elements in the "world"')

        """
        self.reality_status.setColumnCount(3)
        self.reality_status.setRowCount(10)
        for i in range(10):
            self.reality_status.setSpan(i, 0, 1, 2)
        """

        grid.addWidget(self.theme_label,            1, 0)
        grid.addWidget(self.combo_box,              1, 1)
        grid.addWidget(self.begin_button,           2, 0)
        grid.addWidget(self.continue_button,           2, 1)
        grid.addWidget(self.reset_button,           2, 2)
        grid.addWidget(self.help_button,            2, 3)

        grid.addWidget(self.reality_status_label,   3, 0)
        grid.addWidget(self.console_label,          3, 2)
        grid.addWidget(self.logical_links_label,    3, 4)
        editLineSpanTuple = (20, 2)
        grid.addWidget(self.reality_status,    4, 0, *editLineSpanTuple)
        grid.addWidget(self.console,           4, 2, *editLineSpanTuple)
        grid.addWidget(self.logical_links,     4, 4, *editLineSpanTuple)

        self.__makeModelViewLink()

        self.__initButtons()

        self.__updatellModel() #an exemple
        self.__updatersModel() #an exemple

        return grid

    def __initComboBox(self):
        self.combo_box.addItem(self.themeNames[0])
        self.combo_box.addItem(self.themeNames[1])
        self.combo_box.addItem(self.themeNames[2])

        self.combo_box.activated[str].connect(self.onActivatedComboBox)

    def onActivatedComboBox(self, text):
        self.theme = Theme(self.themeNames[self.themeNameDict[text]])
        self.__updateTheme()

    def __makeModelViewLink(self):
        self.logical_links.setModel(self.llModel)
        self.logical_links.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.reality_status.setModel(self.rsModel)
        self.reality_status.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.reality_status.setColumnWidth(0, 300)
        self.reality_status.setColumnWidth(1, 67.9)

    def __initButtons(self):
        self.begin_button.clicked.connect(self.showBeginDialog)
        self.continue_button.clicked.connect(self.continue_activity)
        self.reset_button.clicked.connect(self.reset_activity)
        self.help_button.clicked.connect(self.showHelpDialog)

    def showBeginDialog(self):
        text, ok = QInputDialog.getText(self, 'Begin', 'Enter your demande: \ne.g. "I want a beautiful door"')
        if ok:
            self.inputString = text
            self.begin_activity()

    def begin_activity(self):
        self.editIsVisible = True
        self.console.setText(self.inputString)
        self.console.append("\n*****\nArgumentator begins to argument\n*****\n")
        next(self.themeIterator)
        oneStep = oneStepLogicalFunction() #oneStepLogicalFunction() doit être fourni par la partie logique qui fonctionne comme un générateur Python (yield)
        self.console.append("\n", oneStep,"\n")
        pass

    def continue_activity(self):
        #next(self.themeIterator)
        oneStep = oneStepLogicalFunction()
        self.console.append("\n", oneStep, "\n")
        pass

    def reset_activity(self):
        self.console.setText("")
        self.__updateModels()

    def showHelpDialog(self):
        dialog = QDialog()
        if randint(1,6) % 2 == 1:
            dialog.ui = Help_Dialog1()
        else:
            dialog.ui = Help_Dialog2()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

    def __updateTheme(self):
        """self.theme.name has been modified, we should update the main window"""
        """changes models to update list view and table view, initialize input string and then, configure the console"""
        self.themeIterator = ThemeIterator(self.theme)
        self.inputString = ""
        self.console.setText(self.inputString)
        self.__updateModels()

    def __updateModels(self):
        """updates the models in function of self.theme.name, which means to change the data which is for the model"""
        self.__updatellModel()  # an exemple
        self.__updatersModel()  # an exemple
        pass

    # logical links
    def __updatellModel(self):
        dataLogicalLinks = ["nice_surface <=== burn_off + -wood_wrecked",
                            "nice_surface <=== sanding + -several_layers + -wood_wrecked",
                            "nice_surface <=== filler_compound + -wood_wrecked",
                            "nice_doors <=== repaint + nice_surface",
                            "tough_work <=== burn_off + mouldings + -wire_brush",
                            "wood_wrecked <=== wire_brush + soft_wood",
                            "-nice_surface <=== wood_wrecked"]  # An example
        self.llModel = QStringListModel(dataLogicalLinks)

    # Reality status
    def __updatersModel(self):
        dataRealityStatus = [["The door is repainted", "True"], ["The door is wrecked", "False"],
                             ["The door is beautiful", "True"]]  # An example
        self.rsModel = RsModel(dataRealityStatus)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())