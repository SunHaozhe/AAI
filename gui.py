#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Thurs Jun 22 2017

@author: Haozhe Sun
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, QDesktopWidget, QToolTip
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QWidget):
    """To define the main window of our program"""

    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        """To initialize the main window"""

        #To set up a tooltip for the whole program
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Arguing AI')


        #To creat a push button to quit the program
        quit_btn = QPushButton('Quit', self)
        quit_btn.clicked.connect(QCoreApplication.instance().quit)
        quit_btn.setToolTip('Click to quit')
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.move(900, 600)

        self.resize(1000, 800)
        self.__center()
        self.setWindowTitle('Arguing AI')

        #We can add an icon if we need
        #self.setWindowIcon(QIcon('XXX.png'))

        self.show()


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())