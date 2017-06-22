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
                return link.consequence
            return None  
        if link.link_type == "incompatibility":
            if T in link.incompatibilities:
                return [P.negation for P in link.incompatibilities if P!=T]
            return None  
    
    '''        
    @staticmethod
    def find_all_consequences(link):
        if link.link_type == "causal":
            return link.consequence
        if link.link_type == "incompatibility":
            return [P.negation for P in link.incompatibilities]
        return None
    '''
    
    
    @staticmethod        
    def find_causes(T,link):
        if link.link_type == "causal":
            if T == link.consequence:
                return link.causes
            return None
            
        if link.link_type == "incompatibility":
            if T.negation in link.incompatibilities:
                return [P for P in link.incompatibilities if P!=T.negation]
            return None
    
    @staticmethod          
    def causal_relations(link):
        if link.link_type == "causal":
            yield (link.causes, link.consequence)
        if link.link_type == "incompatibility":
            incomp = link.incompatibilities
            for i in range(len(incomp)):
                yield (incomp[0:i]+incomp[i+1:],incomp[i].negation)
    
    '''
    @staticmethod
    def makes_true(T,link):  
        if link.link_type == "causal":
            if T == link.consequence:
                return all(P.realised for P in link.causes)
            return False
        if link.link_type == "incompatibility":
            if T.negation in link.incompatibilities:
                return all(P.realised for P in link.incompatibilities if P!=T.negation)
            return False
    '''


class Causal_link:
    """Represents a causal link between two lists of predicates."""
    
    def __init__(self, causes, consequence):
        self.causes = causes
        self.consequence = consequence
        self.link_type = "causal"
        for pred in causes:
            pred.forward_links.append(self)
        consequence.backward_links.append(self)
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Causal_Link_(%s <=== %s)"%(self.consequence,self.causes)
    __str__ = __repr__
    #-----------------------------
        
class Incompatibility_link:
    """Represents an incompatibility link between different predicates."""
    
    def __init__(self, incompatibilities):
        self.incompatibilities = incompatibilities
        self.link_type = "incompatibility"
        for pred in incompatibilities:
            pred.forward_links.append(self)
            pred.negation.backward_links.append(self)
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Incompatibility_Link_(%s)"%self.incompatibilities
    __str__ = __repr__
    #-----------------------------
    