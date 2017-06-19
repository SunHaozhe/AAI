# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
def propagation(T):
    """ implements Wordl argumentation """
    L = T.logical_links
    if T.realised == True and L.link_type == causal:
        if all(P.realised for P in L.causes):
            for P in L.consequences:
                P.realised == True
    else:
        for link in L:
            for P in link.consequences:
                for link_deux in P.logical_links:
                    if link.makes_true(self):
                        being_realised = True
                        break
                if not P.realised and being_realised:
                    print("Inferring %s from %s" %(P.name,T.name))
                    make_true(P)

                elif P.realised and not being_realised and not P._init_situation:
                    print("Went back to %s because of %s" %(P.negation.name,T.negation.name))
                    make_true(P.negation)
        
        
def make_true(T):
    """Makes the predicate realised and updates itself and other predicates
    accordingly.
    """
    T.realised = True
    T.conceived = True
    T.negation.realised = False
    T.negation.conceived = False
    propagation(T)
    propagation(T.negation)
    T.make_action()

