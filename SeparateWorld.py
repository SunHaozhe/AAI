# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
class World:
    
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
    
    def makes_true(T,link):  
        if link.link_type == "causal":
            if T in link.consequences:
                if all(P.realised for P in link.causes):
                    return True
            return False
    
    @staticmethod
    def __propagation(T):
        """ implements Wordl argumentation """
        L = T.logical_links
        for link in L:
            consequences = World.find_consequences(T,link)
            if consequences==None:
                continue
            for P in consequences:
                being_realised = False
                for link_deux in P.logical_links:
                    if World.makes_true(P,link):
                        being_realised = True
                        break
                if not P.realised and being_realised:
                    print("Inferring %s from %s" %(P.name,T.name))
                    World.make_true(P)

                elif P.realised and not being_realised and not P.init_situation:
                    print("Went back to %s because of %s" %(P.negation.name,T.negation.name))
                    World.make_true(P.negation)
            
    @staticmethod        
    def make_true(T):
        """Makes the predicate realised and updates itself and other predicates
        accordingly.
        """
        T.realised = True
        T.conceived = True
        T.negation.realised = False
        T.negation.conceived = False
        World.__propagation(T)
        World.__propagation(T.negation)
        T.make_action()

