# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 18:12:33 2017

@author: Tasslehoff
"""

from abduction import Abductor
from debug import Debug

class Argumentator:
    
    def __init__(self,world,mind):
        self.world = world
        self.mind = mind
    
    @staticmethod 
    def __is_conflict(predicate):
        """Checks if predicate is a conflict."""
        if predicate == None:
            return False
        T,N = predicate
        return ((T.seems and N<0) or (T.negation.seems and N>0))
      
        
    def __find_conflict(self):
        """Finds a new conflict in the dictionnary of predicates."""
        predicates = self.world.predicates
        for name in predicates:
            T=predicates[name]
            if Argumentator.__is_conflict((T,T.value)):
                return (T,T.value)
        return None
  
    @staticmethod 
    def __find_mutable_cause(T,N):
        """Finds a mutable cause for predicate (T,N)."""

        for (cause_list,link_type) in Abductor.find_causes(T,shuffle=False):

            # If T is realised we are in diagnostic mode and check if all the 
            # causes are are True before trying to tackle one.
            if N<0:
                if all(cause.seems for cause in cause_list):
                    for cause in cause_list:
                        if not cause.realised and cause.is_mutable(N):
                            return cause
                    for cause in cause_list:
                        if cause.is_mutable(N):
                            return cause
                    
            # Or we are trying to make T happen and look for a way to do so.
            else:
                for cause in cause_list:
                    if (not cause.seems) and cause.is_mutable(N) and cause.realised:
                        return cause
                for cause in cause_list:
                    if not cause.seems and cause.is_mutable(N):
                        return cause

        for (cause_list,link_type) in Abductor.find_causes(T,shuffle=False):

            # If T is realised we are in diagnostic mode and check if all the 
            # causes are are True before trying to tackle one.
            if N<0:
                if all(cause.realised for cause in cause_list):
                    for cause in cause_list:
                        if cause.is_mutable(N):
                            return cause
                    
            # Or we are trying to make T happen and look for a way to do so.
            else:
                for cause in cause_list:
                    if not cause.realised and cause.is_mutable(N):
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
        yield "Do you want to reconsider the value of %s?\n(current value is %d)\n[y/n]" % (R.name,R.value)

        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
                 
        choice = input().lower()
        while choice not in valid:
            yield ("Please respond with 'yes' or 'no' (or 'y' or 'n').")
            choice = input().lower()
        if valid[choice]:
            yield "\nWhat value would you like to give to %s ?\n(current value is %d)" % (R.name, R.value)

            choice = input()
            while not ((len(choice)>1 and choice[0] in ('-', '+') and choice[1:].isdigit()) or choice.isdigit()):
                print("Please enter an integer.")
                choice = input()
            N = int(choice)
            '''
            if N*R.value <= 0 and abs(N)>=abs(R.value):
                for pred_name in self.world.predicates:
                    pred = self.world.predicates[pred_name]
                    if abs(pred.value)<=abs(N):
                        pred.value = 0
            '''
            R.value = N
            R.negation.value = -N
        print("")
        
       
    def __procedure(self,T,N,negated):
        """Starts the Solution/Abduction/Negation/Giving Up procedure on the 
        conflict (T,N), with "negated" indicating if the procedure was started 
        from the negation of a previous conflict.
        """
            
        #Solution : Make T happen if it is possible and value is positive.
        if N>0 and T.seems_possible() and not T.seems:
            print("------> Decision : %s"%T.name)
            T.value = N
            T.negation.value = -N
            T.seems = True
            T.negation.seems = False
            self.world.update_based_on(T)
            self.mind.update_based_on(T)
            return None
        
        #Abduction : find a mutable cause C for T and start procedure for (C,N)
        C = Argumentator.__find_mutable_cause(T,N)

        if C!=None:
            print("Propagating conflict on %s to cause: %s"%(T.name,C.name))
            old_value = C.value
            C.value = N
                #C.negation.value = -N
            new_conflict = self.__procedure(C,C.value,False)
            if new_conflict == "new_realisation":
                C.value = old_value
            if new_conflict != None:
                return new_conflict
            
            return (T,N)

        #Negation : Restart the procedure with the conflict (not T,-N)
        if not negated:
            yield "Negating %s, considering %s"%(T.name,T.negation.name)
            new_conflict = self.__procedure(T.negation,-N, True)
            if new_conflict != None:
                return new_conflict
        
        #Give up : Make v(T) = -N, and reconsider if T is reconsiderable.
        else:
            print("About to give up")
            if (T.negation.seems != T.negation.realised) and (T.seems != T.realised):
                
                T.seems = T.realised
                T.negation.seems = T.negation.realised
                if T.realised:
                    print("Just realised that %s !"%T.name)
                    self.mind.update_based_on(T)
                else:
                    print("Just realised that %s !"%T.negation.name)
                    self.mind.update_based_on(T.negation)
                
                return "new_realisation"
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
        
        yield "\n*********\n**START**\n*********\n"
        conflict = self.__find_conflict()
        while conflict != None:
            Debug.show_truth(self.world)
            (T,N)=conflict
            yield "Considering conflict of intensity %d with %s"%(N,T.name)
            new_conflict = self.__procedure(T,N,False)
            if new_conflict=="new_realisation":
                new_conflict = conflict
            if Argumentator.__is_conflict(new_conflict):
                conflict = new_conflict
            else:
                conflict = self.__find_conflict()
            yield "**Restart**"
            
    
        yield "No conflict found\n\n*******\n**END**\n*******\n"

        

