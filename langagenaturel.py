# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:48:40 2017

@author: Guerric
"""

from Logical import logic

class LangageNaturel:
    
    """Represents an expression understandable for humans"""
    def __init__(self, etape, predicates, dictionnary):
        self.etape = etape
        self.predicates = predicates
        self.dictionnary = dictionnary
        
    def output(self):
        if self.etape == "Initialisation":
            return self.dictionnary['self.predicates.name']
        
        if self.etape == "Abduction":
            return self.dictionnary['self.predicates[0].name'] + self.dictionnary['self.predicates[0].name']
        
        if self.etape == "Negation":
            self.dictionnary['self.predicates.name']
            
        
        
        
        