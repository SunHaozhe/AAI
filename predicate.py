# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 18:06:00 2017

@author: Tasslehoff
"""

class Predicate:
    """Represents a predicate in the extended sense, with value, causes, 
    consequences etc.
    """
    
    def __init__(self, name, value, actionable, realised, default): 
        self.name = name
        self.value = value
        self.actionable = actionable
        self.realised = realised
        self.default = default
        self.reconsiderable = (value!=0)
        self.negation = None
        self.forward_links = []
        self.backward_links = []
    
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Pred_\""+self.name+"\""
    __str__ = __repr__
    #-----------------------------

    
    def is_mutable(self,N):
        """Indicates if the predicate is mutable with intensity N."""
        return (N*self.value<=0 and abs(self.value)<abs(N)) or N*self.value>=0
        
    def is_possible(self):
        """Indicates if the predicate is possible."""
        return ((not self.negation.realised) or self.actionable)
        
    def make_action(self):
        """Makes the action corresponding to the predicate if there is one.
        (to be overwritten for particular instances of this class)
        """
        return