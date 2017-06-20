# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from logical import Logic
import copy

class World:
    
    def __init__(self,predicates,logical_links):
        self.predicates = predicates
        self.logical_links = logical_links
        self.init_situations = {}
        self.past_situations = {}
        self.is_consequence = {}
        for pred_name in self.predicates:
            self.init_situations[pred_name] = self.predicates[pred_name].realised
            self.past_situations[pred_name] = self.init_situations[pred_name]
            self.is_consequence[pred_name] = False
        self.decisions = []

    def __restore_initial_situation(self):
        for pred_name in self.predicates:
            self.past_situations[pred_name] = self.predicates[pred_name].realised
            if self.is_consequence[pred_name]:
                self.predicates[pred_name].realised = self.init_situations[pred_name]    
            
    
    def propagate_forward(self,T,show_inference):
        change = False
        for link in T.logical_links:
            for (causes,consequences) in Logic.causal_relations(link):
                if T in causes and all(c.realised for c in causes):
                    for P in consequences:
                        if not P.realised:
                            self.make_true(P,show_inference)
                            change = True
                            if not self.past_situations[P.name]:
                                if show_inference:
                                    print("Inferring %s from %s" %(P.name,T.name))
                                self.past_situations[P.name] = True
        '''
        print("#########")
        for pred_name in self.predicates:
            print(pred_name,"  |  ",self.predicates[pred_name].realised)
        print("#########",change,"#########")
        '''
        return change


    def update_based_on(self,T):
        
        if T.negation.name in self.decisions:
            self.decisions.remove(T.negation.name)
                   
        self.__restore_initial_situation()
        
        for pred_name in self.decisions:
            self.make_true(self.predicates[pred_name],False)
        
        self.make_true(T,True)
        self.decisions.append(T.name)
        
        

                      
    def make_true(self,T,show_inference):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.negation.realised = False
        self.propagate_forward(T,show_inference)
        T.make_action()


