# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:10:22 2017

@author: Tasslehoff
"""
import random
from SeparateWorld import World

class Abductor:
    
    
    def find_causes(T):
        link_indices = list(range(len(T.logical_links)))
        random.shuffle(link_indices)
        for link_index in link_indices:
            link = T.logical_links[link_index]
            causes = World.find_causes(T,link)
            if causes != None:
                random.shuffle(causes)
                yield causes