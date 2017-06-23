# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 18:12:33 2017

@author: Tasslehoff
"""

from abduction import Abductor
from debug import Debug

class Argumentator:
    
    def __init__(self,world):
        self.world = world
        self.defaults = 0# defaults
    
    @staticmethod 
    def __is_conflict(predicate):
        """Checks if predicate is a conflict."""
        if predicate == None:
            return False
        T,N = predicate
        return ((T.realised and N<0) or (T.negation.realised and N>0))
      
        
    def __find_conflict(self):
        """Finds a new conflict in the dictionnary of predicates."""
        predicates = self.world.predicates
        for name in predicates:
            T=predicates[name]
            if Argumentator.__is_conflict((T,T.value)):
                return (T,T.value)
        return None
  
    @staticmethod    
    def __seems_realised(T,consider_default=True):
        if not consider_default:
            return T.realised
        return (T.realised and T.default !=-1) or T.default==1

    @staticmethod 
    def __find_mutable_cause(T,N):
        """Finds a mutable cause for predicate (T,N)."""

        for cause_list in Abductor.find_causes(T):

            # If T is realised we are in diagnostic mode and check if all the 
            # causes are are True before trying to tackle one.
            for consider_default in (True,False):
                if N<0:
                    if all(Argumentator.__seems_realised(cause,consider_default) for cause in cause_list):
                        for cause in cause_list:
                            if cause.is_mutable(N):
                                return cause
                                
                # Or we are trying to make T happen and look for a way to do so.
                else:
                    for cause in cause_list:
                        if not Argumentator.__seems_realised(cause,consider_default) and cause.is_mutable(N):
                            return cause
        return None
        
         
    def __reconsider(self,T):
        """Prompts the user to reconsider the value of a predicate if he wishes
        to do so.
        """
        if T.name[0]=='-':
            R = T.negation
        else:
            R = T
        print("Do you want to reconsider the value of %s?" % R.name)
        print("(current value is %d)" % R.value)
        print("[y/n]")
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
                 
        choice = input().lower()
        while choice not in valid:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
            choice = input().lower()
        if valid[choice]:
            print("\nWhat value would you like to give to %s ?" % R.name)
            print("(current value is %d)" % R.value)
            choice = input()
            while not ((len(choice)>1 and choice[0] in ('-', '+') and choice[1:].isdigit()) or choice.isdigit()):
                print("Please enter an integer.")
                choice = input()
            R.value = int(choice)
            R.negation.value = -int(choice)
        print("")
        
       
    def __procedure(self,T,N,negated):
        """Starts the Solution/Abduction/Negation/Giving Up procedure on the 
        conflict (T,N), with "negated" indicating if the procedure was started 
        from the negation of a previous conflict.
        """
        
        T.default = 0
        T.negation.default = 0
        #Solution : Make T happen if it is possible and value is positive.
        if N>0 and (not T.realised) and T.is_possible():
            print("------> Decision : %s"%T.name)
            self.world.update_based_on(T)
            T.value = N
            T.negation.value = -N
            return None
        
        #Abduction : find a mutable cause C for T and start procedure for (C,N)
        C = Argumentator.__find_mutable_cause(T,N)

        if C!=None:
            print("Propagating conflict on %s to cause: %s"%(T.name,C.name))
            if abs(C.value)<abs(N):
                C.value = N
                C.negation.value = -N
            new_conflict = self.__procedure(C,C.value,False)
            if new_conflict != None:
                return new_conflict 

            return (T,N)

        #Negation : Restart the procedure with the conflict (not T,-N)
        if not negated:
            print("Negating %s, considering %s"%(T.name,T.negation.name))
            new_conflict = self.__procedure(T.negation,-N, True)
            if new_conflict != None:
                return new_conflict
        
        #Give up : Make v(T) = -N, and reconsider if T is reconsiderable.
        else:
            if T.realised:
                print("Giving up: %s is stored with necessity %d"%(T.name,-N))
            else:
                print("Giving up: %s is stored with necessity %d"%(T.negation.name,N))
            T.value = -N
            T.negation.value = N
            if T.reconsiderable:
                self.__reconsider(T.negation)
            return None


    def argue(self):
        """Starts the whole CAN procedure on the specified dictionnary of 
        predicates.
        """
        
        print("\n*********\n**START**\n*********\n")
        conflict = self.__find_conflict()
        while conflict != None:
            Debug.show_truth(self.world)
            (T,N)=conflict
            print("Considering conflict of intensity %d with %s"%(N,T.name))
            new_conflict = self.__procedure(T,N,False)
            if Argumentator.__is_conflict(new_conflict):
                conflict = new_conflict
            else:
                conflict = self.__find_conflict()
            print("**Restart**")
            
    
        print("No conflict found\n\n*******\n**END**\n*******\n")

        

