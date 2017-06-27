<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:44:07 2017

@author: Justin
"""

from logical import Logic
from langagenaturel import LangageNaturel

class Mind:
    
    def __init__(self,predicates,logical_links, dictionary):
        self.dictionary = dictionary
        self.predicates = predicates
        self.logical_links = logical_links
        self.init_situation = []
        self.previous_situation =  {}
        self.infered_from = {}
        self.has_infered = {}
        for pred_name in self.predicates:           
            if self.predicates[pred_name].seems:
                self.init_situation.append(pred_name)
                self.previous_situation[pred_name]=True
            self.infered_from[pred_name]=set()
            self.has_infered[pred_name]=set()
        self.update_based_on(None)
        
                
    def update_based_on(self,T):
              
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].seems:
                self.previous_situation[pred_name]=True
            self.predicates[pred_name].seems = False
            
                
        if T!=None:         
            if T.negation.name in self.init_situation:
                self.init_situation.remove(T.negation.name)    
            self.init_situation.append(T.name)
            
            
        change = True
        while change:
            change = False
            for p in self.init_situation[::-1]:
                if not self.predicates[p].negation.seems:
                    self.predicates[p].seems = True
                    marked = self.propagate_forward(self.predicates[p],set([p]))
                    if marked != None:
                        for pred_name in marked:
                            if not self.predicates[pred_name].seems:
                                self.predicates[pred_name].seems = True
                                change = True
                            
                            
        for p in self.predicates:
            if self.predicates[p].realised and not self.predicates[p].negation.seems:
                self.predicates[p].seems = True                       
            if self.predicates[p].seems and p not in self.previous_situation :
                language = LangageNaturel("Mind", self.predicates[p], self.dictionary)
                print(language.output())
                #print("(Mind) Inferring %s." %(p))
                      
             
    def propagate_forward(self,T,marked):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                    if conseq != T and all(c.seems or (c.name in marked) for c in causes):
                        if conseq.negation.seems or (conseq.negation.name in marked):
                            return None
                        if not conseq.name in marked:
                            marked.add(conseq.name)
                            if self.propagate_forward(conseq,marked)==None:
                                return None
        return marked



        
=======
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:44:07 2017

@author: Justin
"""

from logical import Logic
from langagenaturel import LangageNaturel

class Mind:
    
    def __init__(self,predicates,logical_links, dictionary):
        self.dictionary = dictionary
        self.predicates = predicates
        self.logical_links = logical_links
        self.init_situation = []
        self.previous_situation =  {}
        self.infered_from = {}
        self.has_infered = {}
        for pred_name in self.predicates:           
            if self.predicates[pred_name].seems:
                self.init_situation.append(pred_name)
                self.previous_situation[pred_name]=True
            self.infered_from[pred_name]=set()
            self.has_infered[pred_name]=set()
        self.update_based_on(None)
        
                
    def update_based_on(self,T):
              
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].seems:
                self.previous_situation[pred_name]=True
            self.predicates[pred_name].seems = False
            
                
        if T!=None:         
            if T.negation.name in self.init_situation:
                self.init_situation.remove(T.negation.name)    
            self.init_situation.append(T.name)
            
            
        change = True
        while change:
            change = False
            for p in self.init_situation[::-1]:
                if not self.predicates[p].negation.seems:
                    self.predicates[p].seems = True
                    marked = self.propagate_forward(self.predicates[p],set([p]))
                    if marked != None:
                        for pred_name in marked:
                            if not self.predicates[pred_name].seems:
                                self.predicates[pred_name].seems = True
                                change = True
                            
                            
        for p in self.predicates:
            if self.predicates[p].realised and not self.predicates[p].negation.seems:
                self.predicates[p].seems = True                       
            if self.predicates[p].seems and p not in self.previous_situation :
                language = LangageNaturel("Mind", self.predicates[p], self.dictionary)
                print(language.output())
                #print("(Mind) Inferring %s." %(p))
                      
             
    def propagate_forward(self,T,marked):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                    if conseq != T and all(c.seems or (c.name in marked) for c in causes):
                        if conseq.negation.seems or (conseq.negation.name in marked):
                            return None
                        if not conseq.name in marked:
                            marked.add(conseq.name)
                            if self.propagate_forward(conseq,marked)==None:
                                return None
        return marked



        
>>>>>>> origin/World_forward_propagation
        