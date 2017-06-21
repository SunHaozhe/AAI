# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:03:21 2017

@author: Tasslehoff
"""

class Logical_link:
    """Represents a logical link of any kind between different predicates."""
    
        
class Causal_link(Logical_link):
    """Represents a causal link between two lists of predicates."""
    
    def __init__(self, causes, consequences):
        self.causes = causes
        self.consequences = consequences
        self.link_type = "causal"
    
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Logic_(%s --> %s)"%(self.causes,self.consequences)
    __str__ = __repr__
    #-----------------------------
        
class Incompatibility_link(Logical_link):
    """Represents an incompatibility link between different predicates."""
    
    def __init__(self, words):
        self.words = words
        self.link_type = "incompatibility"
        
    