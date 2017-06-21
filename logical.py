# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:03:21 2017

@author: Tasslehoff
"""

class Logic:
    
    @staticmethod
    def find_consequences(T,link):
        if link.link_type == "causal":
            if T in link.causes:
                return link.consequences
            return None     
    
    @staticmethod        
    def find_causes(T,link):
        if link.link_type == "causal":
            if T in link.consequences:
                return link.causes
            return None
            
    @staticmethod          
    def causal_relations(link):
        if link.link_type == "causal":
            yield (link.causes, link.consequences)
    
    @staticmethod
    def makes_true(T,link):  
        if link.link_type == "causal":
            if T in link.consequences:
                if all(P.realised for P in link.causes):
                    return True
            return False

        
class Causal_link:
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
        
    