<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:49:20 2017

@author: Justin
"""

class Debug:
    
    DEBUG = False
    @classmethod
    def do_nothing(*arg):
        pass
    @classmethod
    def show_truth(cls, world):
        for pred_name in world.predicates:
            if pred_name[0]!="-":
                pred = world.predicates[pred_name]
                negpred = world.predicates[pred_name].negation
                l = len(pred_name)
                real = pred.seems
                rl = len(str(pred.seems))
                negreal = negpred.seems
                nrl = len(str(negpred.seems))
                print("-"*50)
                print(pred_name," "*(20-l)+"|   ", real," "*(10-rl)+"|   ", pred.value)
                print("-"*50)
                print("-"+pred_name," "*(19-l)+"|   ", negreal," "*(10-nrl)+"|   ", negpred.value)
                print("-"*50)
                print("-"*50)
                
    if not DEBUG:
=======
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:49:20 2017

@author: Justin
"""

class Debug:
    
    DEBUG = False
    @classmethod
    def do_nothing(*arg):
        pass
    @classmethod
    def show_truth(cls, world):
        for pred_name in world.predicates:
            if pred_name[0]!="-":
                pred = world.predicates[pred_name]
                negpred = world.predicates[pred_name].negation
                l = len(pred_name)
                real = pred.seems
                rl = len(str(pred.seems))
                negreal = negpred.seems
                nrl = len(str(negpred.seems))
                print("-"*50)
                print(pred_name," "*(20-l)+"|   ", real," "*(10-rl)+"|   ", pred.value)
                print("-"*50)
                print("-"+pred_name," "*(19-l)+"|   ", negreal," "*(10-nrl)+"|   ", negpred.value)
                print("-"*50)
                print("-"*50)
                
    if not DEBUG:
>>>>>>> origin/World_forward_propagation
        show_truth = do_nothing