<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from logical import Logic
from langagenaturel import LangageNaturel

class World:
    
    def __init__(self,predicates,logical_links, dictionary):
        self.dictionary = dictionary
        self.predicates = predicates
        self.logical_links = logical_links
        self.init_situation = []
        self.previous_situation =  {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.init_situation.append(pred_name)
        self.update_based_on(None)
        
               
    def update_based_on(self,T):
              
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.previous_situation[pred_name]=True
            self.predicates[pred_name].realised = False
            
                
        if T!=None:         
            if T.negation.name in self.init_situation:
                self.init_situation.remove(T.negation.name)    
            self.init_situation.append(T.name)
            
            
        change = True
        while change:
            change = False
            for p in self.init_situation[::-1]:
                if not self.predicates[p].negation.realised:
                    self.predicates[p].realised = True
                    marked = self.propagate_forward(self.predicates[p],set([p]))
                    if marked != None:
                        for pred_name in marked:
                            if not self.predicates[pred_name].realised:
                                self.predicates[pred_name].realised = True
                                change = True
                            
                            
        for p in self.predicates:                        
            if self.predicates[p].realised and p not in self.previous_situation:
                """language = LangageNaturel("World", self.predicates[p], self.dictionary)
                print(language.output())"""
                #print("(World) Inferring %s." %(p))
                      
             
    def propagate_forward(self,T,marked):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                    
                    if conseq != T and all(c.realised or (c.name in marked) for c in causes):
                        if conseq.negation.realised or (conseq.negation.name in marked):
                            return None
                        if not (conseq.name in marked or conseq.realised):
                            marked.add(conseq.name)
                            if self.propagate_forward(conseq,marked)==None:
                                return None
        return marked
                        
                
        
=======
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from logical import Logic
from langagenaturel import LangageNaturel

class World:
    
    def __init__(self,predicates,logical_links, dictionary):
        self.dictionary = dictionary
        self.predicates = predicates
        self.logical_links = logical_links
        self.init_situation = []
        self.previous_situation =  {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.init_situation.append(pred_name)
        self.update_based_on(None)
        
               
    def update_based_on(self,T):
              
        self.previous_situation = {}
        for pred_name in self.predicates:
            if self.predicates[pred_name].realised:
                self.previous_situation[pred_name]=True
            self.predicates[pred_name].realised = False
            
                
        if T!=None:         
            if T.negation.name in self.init_situation:
                self.init_situation.remove(T.negation.name)    
            self.init_situation.append(T.name)
            
            
        change = True
        while change:
            change = False
            for p in self.init_situation[::-1]:
                if not self.predicates[p].negation.realised:
                    self.predicates[p].realised = True
                    marked = self.propagate_forward(self.predicates[p],set([p]))
                    if marked != None:
                        for pred_name in marked:
                            if not self.predicates[pred_name].realised:
                                self.predicates[pred_name].realised = True
                                change = True
                            
                            
        for p in self.predicates:                        
            if self.predicates[p].realised and p not in self.previous_situation:
                """language = LangageNaturel("World", self.predicates[p], self.dictionary)
                print(language.output())"""
                #print("(World) Inferring %s." %(p))
                      
             
    def propagate_forward(self,T,marked):
        for link in T.forward_links:
            for (causes,conseq) in Logic.causal_relations(link):
                    
                    if conseq != T and all(c.realised or (c.name in marked) for c in causes):
                        if conseq.negation.realised or (conseq.negation.name in marked):
                            return None
                        if not (conseq.name in marked or conseq.realised):
                            marked.add(conseq.name)
                            if self.propagate_forward(conseq,marked)==None:
                                return None
        return marked
                        
                
        
>>>>>>> origin/World_forward_propagation
