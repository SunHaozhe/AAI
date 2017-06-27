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
        self.dictionary = dictionary
        
    def output(self):
        if self.etape == "Initialisation":
            return "Il faudrait que " + self.dictionary['self.predicates.name'] + "..."
        
        if self.etape == "Abduction":
            return "Pour que " + self.dictionary['self.predicates[0].name'] + ", il est nécessaire que " + self.dictionnary['self.predicates[1].name'] + "."
        
        if self.etape == "Negation":
            return self.dictionary['self.predicates.name']
        
        if self.etape == "Discovery":
            return "Je viens de réaliser que " + self.dictionary['self.predicates.name'] + " !"
        
        if self.etape == "Solution":
            return "J'ai trouvé la solution !"
        
        if self.etape == "Surrender":
            return "Je ne trouve pas de solution."
        
            
            
        
        
        
        