# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 19:10:22 2017

@author: Tasslehoff
"""
import random
from logical import Logic

class Abductor:
    @classmethod 
    def find_causes(cls,T,shuffle=True):
        l = len(T.backward_links)
        causal_link_indices = [i for i in range(l) if T.backward_links[i].link_type=="causal"]
        other_link_indices = [i for i in range(l) if i not in causal_link_indices]
        
        
        if shuffle:
            random.shuffle(causal_link_indices)
            random.shuffle(other_link_indices)
        link_indices = causal_link_indices+other_link_indices
        for link_index in link_indices:
            link = T.backward_links[link_index]
            causes = Logic.find_causes(T,link)
            if causes != None:
                if shuffle:
                    random.shuffle(causes)
                yield causes,link.link_type
                
#causes = Logic.find_causes(T,l)
