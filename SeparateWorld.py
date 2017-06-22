# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from logical import Logic

class World:
    
    def __init__(self,predicates,logical_links,init_situation):
        self.predicates = predicates
        self.logical_links = logical_links
        self.decisions = []
        self.init_situation = init_situation
        self.previous_situation = {}
               
    def update_based_on(self,T):
        
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.previous_situation[pred_name]=True
        
        if T.negation.name in self.decisions:
            self.decisions.remove(T.negation.name)
            
        self.decisions.append(T.name)
        for pred_name in self.predicates:
            self.predicates[pred_name].realised = (pred_name in self.init_situation)
        for p in self.init_situation:
                self.make_true(self.predicates[p])
        for p in self.decisions[::-1]:
                self.make_true(self.predicates[p])
                
             
    def propagate_forward(self,T):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                if conseq != T and all(c.realised for c in causes):
                    if not conseq.realised:
                        if conseq.name not in self.previous_situation:
                            print("Inferring %s." %(conseq.name))
                        self.make_true(conseq)
                        
                      
    def make_true(self,T):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.negation.realised = False
        self.propagate_forward(T)
        T.make_action()
        
