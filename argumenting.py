# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 18:12:33 2017

@author: Tasslehoff
"""


import random

class Argumentator:
    
    @staticmethod 
    def __is_conflict(predicate):
        """Checks if predicate is a conflict."""
        if predicate == None:
            return False
        T,N = predicate
        return ((T.realised and N<0) or (T.negation.realised and N>0))
        
    @staticmethod         
    def __find_conflict(predicates):
        """Finds a new conflict in the dictionnary of predicates."""
        for name in predicates:
            T=predicates[name]
            if Argumentator.__is_conflict((T,T.value)):
                return (T,T.value)
        return None
    
    @staticmethod     
    def __find_cause(T,N):
        """Finds a mutable cause for predicate (T,N)."""

        link_indices = list(range(len(T.logical_links)))
        random.shuffle(link_indices)
        for link_index in link_indices:
            cause_list = T.logical_links[link_index].find_causes(T)
            if cause_list==None:
                continue
            
            cause_indices = list(range(len(cause_list)))
            random.shuffle(cause_indices)
            
            # If T is realised we are in diagnostic mode and check if all the 
            # causes are are True before trying to tackle one.
            if N<0:
                if all(cause.conceived for cause in cause_list):
                    for cause_index in cause_indices:
                        cause = cause_list[cause_index]
                        if cause.is_mutable(N):
                            return cause
            # Or we are trying to make T happen and look for a way to do so.
            else:
                for cause_index in cause_indices:
                    cause = cause_list[cause_index]
                    if not cause.conceived and cause.is_mutable(N):
                        return cause
        return None
        
    @staticmethod    
    def __reconsider(T):
        """Prompts the user to reconsider the value of a predicate if he wishes
        to do so.
        """
        print("Do you want to reconsider the value of %s?" % T.name)
        print("(current value is %d)" % T.value)
        print("[y/n]")
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
                 
        choice = input().lower()
        while choice not in valid:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
            choice = input().lower()
        if valid[choice]:
            print("\nWhat value would you like to give to %s ?" % T.name)
            print("(current value is %d)" % T.value)
            choice = input()
            while not ((len(choice)>1 and choice[0] in ('-', '+') and choice[1:].isdigit()) or choice.isdigit()):
                print("Please enter an integer.")
                choice = input()
            T.value = int(choice)
            T.negation.value = -int(choice)
        print("")
        
    
    @staticmethod    
    def __procedure(T,N,negated):
        """Starts the Solution/Abduction/Negation/Giving Up procedure on the 
        conflict (T,N), with "negated" indicating if the procedure was started 
        from the negation of a previous conflict.
        """
        #Solution : Make T happen if it is possible and value is positive.
        if N>0 and T.is_possible():
            print("------> Decision : %s"%T.name)
            T.make_true()
            T.value = N
            T.negation.value = -N
            return None
        
        #Abduction : find a mutable cause C for T and start procedure for (C,N)
        C = Argumentator.__find_cause(T,N)
        if C!=None:
            print("Propagating conflict on %s to cause: %s"%(T.name,C.name))
            new_conflict = Argumentator.__procedure(C,N,False)
            if new_conflict != None:
                return new_conflict 
            else:
                return (T,N)
        
        #Negation : Restart the procedure with the conflict (not T,-N)
        if not negated:
            print("Negating %s, considering %s"%(T.name,T.negation.name))
            new_conflict = Argumentator.__procedure(T.negation,-N, True)
            if new_conflict != None:
                return new_conflict
        
        #Give up : Make v(T) = -N, and reconsider if T is reconsiderable.
        else:
            print(" Giving up: %s is stored with necessity %d"%(T.negation.name,N))
            T.value = -N
            T.negation.value = N
            if T.reconsiderable:
                Argumentator.__reconsider(T.negation)
            return (T,-N)
        return (T,N)

        
    @staticmethod     
    def argue(predicates):
        """Starts the whole CAN procedure on the specified dictionnary of 
        predicates.
        """
        print("\n*********\n**START**\n*********\n")
        
        conflict = Argumentator.__find_conflict(predicates)
        while conflict != None:
            (T,N)=conflict
            print("Considering conflict of intensity %d with %s"%(N,T.name))
            new_conflict = Argumentator.__procedure(T,N,False)
            if Argumentator.__is_conflict(new_conflict):
                conflict = new_conflict
            else:
                conflict = Argumentator.__find_conflict(predicates)
            print("**Restart**")
            
    
        print("No conflict found\n\n*******\n**END**\n*******\n")

        

