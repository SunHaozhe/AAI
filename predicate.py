# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 18:06:00 2017

@author: Tasslehoff
"""

class Predicate:
    """Represents a predicate in the extended sense, with value, causes, 
    consequences etc.
    """
    
    def __init__(self, name, value, actionable, realised, conceived): 
        self.name = name
        self.value = value
        self.actionable = actionable
        self.realised = realised
        self._init_situation = realised
        self.conceived = conceived
        self.reconsiderable = (value!=0)
        self.negation = None
        self.logical_links = []
    
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Pred_\""+self.name+"\""
    __str__ = __repr__
    #-----------------------------

    
    def is_mutable(self,N):
        """Indicates if the predicate is mutable with intensity N."""
        return N*self.value<=0 and abs(self.value)<abs(N)
        
    def is_possible(self):
        """Indicates if the predicate is possible."""
        return (not self.negation.realised) or self.actionable
    
    def propagate_change(self):
        """Propagates the update of status forward in the rule set."""
        for link in self.logical_links:
            link.propagate_change(self)
        
    def update(self,changed_cause):
        """Updates the status according to the rules and current status of
        causes.
        """
        being_realised = False
        for link in self.logical_links:
            if link.makes_true(self):
                being_realised = True
                break
        if not self.realised and being_realised:
            print("Inferring %s from %s" %(self.name,changed_cause.name))
            self.make_true()

        elif self.realised and not being_realised and not self._init_situation:
            print("Went back to %s because of %s" %(self.negation.name,changed_cause.negation.name))
            self.negation.make_true()
        
    def make_true(self):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        self.realised = True
        self.conceived = True
        self.negation.realised = False
        self.negation.conceived = False
        self.propagate_change()
        self.negation.propagate_change()
        self.make_action()
        
    def make_action(self):
        """Makes the action corresponding to the predicate if there is one.
        (to be overwritten for particular instances of this class)
        """
        return