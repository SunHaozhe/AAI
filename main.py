# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 18:24:40 2017

@author: Tasslehoff
"""

from preprocessing import Preprocessor
from argumenting import Argumentator
from SeparateWorld import World
from mind import Mind
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        message = ("This script needs one argument : the path to the file " 
                   "containing the predicate data.")
        print(message)
        sys.exit()
    filename = sys.argv[1]

    predicates,logical_links, dictionary = Preprocessor.setup_data(filename)
    world = World(predicates,logical_links, dictionary, 2)
    mind = Mind(predicates,logical_links, dictionary, 2)
    argumentator = Argumentator(world,mind,dictionary, 2)
    argumentator.argue()

"""
from preprocessing import Preprocessor
from argumenting import Argumentator
from SeparateWorld import World
from mind import Mind
filename = "proportionnelle.pl"

predicates,logical_links, dictionary = Preprocessor.setup_data(filename)
world = World(predicates,logical_links, dictionary, 2)
mind = Mind(predicates,logical_links, dictionary, 2)
argumentator = Argumentator(world,mind,dictionary, 2)
argumentator.argue()
"""

