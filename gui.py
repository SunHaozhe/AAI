#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Thurs Jun 22 2017

@author: Haozhe Sun
"""

import sys
from PyQt5.QtWidgets import (QPushButton, QApplication, QMessageBox, QDesktopWidget,
                            QToolTip, QMainWindow,QAction, qApp, QTextEdit, QGridLayout,
                             QLabel, QLineEdit, QWidget, QHBoxLayout, QComboBox, QFrame,
                             QGroupBox, QListWidget, QTableWidget, QListView, QTableView,
                             QAbstractItemView, QDialog)
from PyQt5.QtCore import QCoreApplication, QSize, QMetaObject
from PyQt5.QtGui import QIcon, QFont
from model_view import *
from dialogs import *
from random import randint


class MainWindow(QMainWindow):
    """To define the main window of our program"""

    def __init__(self):
        super().__init__()
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
        self.setWindowTitle('Arguing AI')

        #We can add an icon if we need
        #self.setWindowIcon(QIcon('XXX.png'))

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
        self.pause_button = QPushButton("Pause",self)
        self.reset_button = QPushButton("Reset",self)
        self.help_button  = QPushButton("Help", self)

        self.reality_status_label   = QLabel("Reality status :",self)
        self.console_label          = QLabel("Console :", self)
        self.logical_links_label    = QLabel("Logical links :",self)
        self.reality_status    = QTableView(self)
        self.console           = QTextEdit()
        self.logical_links     = QListView(self)
        self.console.setReadOnly(True)

        """
        self.reality_status.setColumnCount(3)
        self.reality_status.setRowCount(10)
        for i in range(10):
            self.reality_status.setSpan(i, 0, 1, 2)
        """

        grid.addWidget(self.theme_label,            1, 0)
        grid.addWidget(self.combo_box,              1, 1)
        grid.addWidget(self.begin_button,           2, 0)
        grid.addWidget(self.pause_button,           2, 1)
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

        return grid

    def __initComboBox(self):
        self.combo_box.addItem("Doors")
        self.combo_box.addItem("Tennis")
        self.combo_box.addItem("Proportional")

    def __makeModelViewLink(self):
        self.logical_links.setModel(llModel)
        self.logical_links.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.reality_status.setModel(rsModel)
        self.reality_status.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def __initButtons(self):
        self.help_button.clicked.connect(self.showHelpDialog)

    def showHelpDialog(self):
        dialog = QDialog()
        if randint(1,6) % 2 == 1:
            dialog.ui = Ui_Dialog1()
        else:
            dialog.ui = Ui_Dialog2()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())