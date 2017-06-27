#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Monday Jun 26 2017

@author: Haozhe Sun
"""

from preprocessing import Preprocessor
from argumenting import Argumentator
import sys
from gui import *
import threading

"""
def t1_function():
    Argumentator.argue(predicates)

def t2_function():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
"""

if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        message = ("This script needs one argument : the path to the file " 
                   "containing the predicate data.")
        print(message)
        sys.exit()
    filename = sys.argv[1]
    predicates,logical_links = Preprocessor.setup_data(filename)
    """
    """
    #terminal thread
    t1 = threading.Thread(target=t1_function, name='terminalThread')
    t1.start()
    """

    #graphic interface
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())


