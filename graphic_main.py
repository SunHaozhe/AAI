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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        message = ("This script needs one argument : the path to the file " 
                   "containing the predicate data.")
        print(message)
        sys.exit()
    filename = sys.argv[1]
    predicates,logical_links = Preprocessor.setup_data(filename)
    #Argumentator.argue(predicates)

    #graphic interface
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

