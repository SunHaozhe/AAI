# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from logical import Logic



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
            self.predicates[pred_name].realised = self.init_situations[pred_name]

   
    def propagate(self,T):
        """ implements World argumentation """
        change = False
        for link in T.logical_links:
            consequences = Logic.find_consequences(T,link)
            if consequences==None:
                continue
            for P in consequences:
                being_realised = False
                for conseq_link in P.logical_links:
                    if Logic.makes_true(P,conseq_link):
                        being_realised = True
                        break
                if not P.realised and being_realised:
                    print("Inferring %s from %s" %(P.name,T.name))
                    self.make_true(P)

                elif P.realised and not being_realised and not self.init_situations[P.name]:
                    print("Went back to %s because of %s" %(P.negation.name,T.negation.name))
                    self.make_true(P.negation)
        if change:
            self.propagate(T)


                      
    def make_true(self,T):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.negation.realised = False
        self.propagate(T)
        self.propagate(T.negation)
        T.make_action()


