# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


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

    def __restore_initial_situation(self):
        for pred_name in self.predicates:
            self.past_situations[pred_name] = self.predicates[pred_name].realised
            if self.is_consequence[pred_name]:
                self.predicates[pred_name].realised = self.init_situations[pred_name]
            

    def find_consequences(T,link):
        if link.link_type == "causal":
            if T in link.causes:
                return link.consequences
            return None
            
            
    def find_causes(T,link):
        if link.link_type == "causal":
            if T in link.consequences:
                return link.causes
            return None
            
    def causal_relations(link):
        if link.link_type == "causal":
            yield link.causes, link.consequences
    
    def makes_true(T,link):  
        if link.link_type == "causal":
            if T in link.consequences:
                if all(P.realised for P in link.causes):
                    return True
            return False
    
    def check_all_links(self,T):
        change = False
        for link_name in self.logical_links:
            link = self.logical_links[link_name]
            for causes,consequences in World.causal_relations(link):
                if all(P.realised for P in causes):
                    for P in consequences:
                        if not P.realised:
                            self.make_true(P,True)
                            change = True
                            if not self.past_situations[P.name]:
                                print("Inferring %s from %s" %(P.name,T.name))
                                self.past_situations[P.name] = True
        return change


    def update_based_on(self,T):
        self.make_true(T,False)
        self.__restore_initial_situation()
        change = self.check_all_links(T)
        while change:
            change = self.check_all_links(T)
                
                      
    def make_true(self,T,is_consequence):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.negation.realised = False
        self.is_consequence[T.name] = is_consequence
        self.is_consequence[T.negation.name] = is_consequence
        T.make_action()

