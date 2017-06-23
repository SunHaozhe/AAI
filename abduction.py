# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:10:22 2017

@author: Tasslehoff
"""
import random
from logical import Logic

class Abductor:
    @classmethod
    def find_causes(cls, T,shuffle=False):
        link_indices = list(range(len(T.backward_links)))
        if shuffle:
            random.shuffle(link_indices)
        for link_index in link_indices:
            link = T.backward_links[link_index]
            causes = Logic.find_causes(T,link)
            if causes != None:
                if shuffle:
                    random.shuffle(causes)
                yield causes,link.link_type
                
#causes = Logic.find_causes(T,l)