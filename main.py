# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 18:24:40 2017

@author: Tasslehoff
"""

from preprocessing import Preprocessor
from argumenting import Argumentator
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        message = ("This script needs one argument : the path to the file " 
                   "containing the predicate data.")
        print(message)
        sys.exit()
    filename = sys.argv[1]
    predicates = Preprocessor.setup_data(filename)
    Argumentator.argue(predicates)

"""
from preprocessing import Preprocessor
from argumenting import Argumentator
filename = "doors.pl"
predicates,logical_links = Preprocessor.setup_data(filename)
Argumentator.argue(predicates)
"""