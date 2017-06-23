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
        self.previous_situation =  {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.init_situation.append(pred_name)
                self.previous_situation[pred_name]=True
        self.update_based_on(None)
        
               
    def update_based_on(self,T):
        
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.previous_situation[pred_name]=True
                
        if T!=None:
            if T.negation.name in self.decisions:
                self.decisions.remove(T.negation.name)     
            self.decisions.append(T.name)
    
        for pred_name in self.predicates:
            self.predicates[pred_name].realised = False
     
        for p in self.decisions[::-1]+self.init_situation:
                if not self.predicates[p].negation.realised:
                    self.predicates[p].realised = True
                    self.propagate_forward(self.predicates[p])
                    
        change = True
        sure = []
        while change:
            change = False
            for p in sure+self.decisions[::-1]+self.init_situation:
                if not self.predicates[p].negation.realised:
                    self.predicates[p].realised = True
                    self.propagate_forward(self.predicates[p])
                    
            for p in self.predicates:
                if self.predicates[p].realised and not self.predicates[p].negation.realised:
                    if p not in sure:
                        #if conseq.name not in self.previous_situation:
                        print("Inferring %s." %(p))
                        sure.append(p)
                        change = True
                else:
                    self.predicates[p].realised = False
                    self.predicates[p].negation.realised = False
            
        for p in sure+self.decisions[::-1]+self.init_situation:
                if not self.predicates[p].negation.realised:
                    self.predicates[p].realised = True
                    self.propagate_forward(self.predicates[p],True)
             
    def propagate_forward(self,T,consistent = False):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                if conseq != T and all(c.realised for c in causes):
                    if not conseq.realised and (not consistent or (not conseq.negation.realised)):
                        conseq.realised = True
                        self.propagate_forward(conseq)
                        
                      
    def make_true(self,T):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.negation.realised = False
        self.propagate_forward(T)
        T.make_action()
        
