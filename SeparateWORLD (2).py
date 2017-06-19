
# coding: utf-8

# In[3]:


"""
Created on Fri Jun 16 10:23:18 2017

@author: Justin
"""

import re
from predicate import Predicate
from logical import Causal_link

class Preprocessor:
    """Preprocessing for converting the textual data to Python objects."""
    
    @staticmethod
    def __text_init(filename):
        """Reads the textual data end stores it in the returned dictionnary."""
        
        return_dict = {}
    
        predicates = set()
        
        with open(filename, "r") as file: 
            text = file.read() 
        
        # Find the language and keep the part of the text with the relevent
        # information.
        pattern="\n\s*language\(\'(\w*)\'\)(.*)$"
        language,text = re.findall(pattern, text, flags=re.DOTALL)[0]
        return_dict['language']=language
        text = re.sub("(?:^\s*%.*?$)|(?:%+.*?%+)", "", text, flags=re.MULTILINE)
        
        # Store the logical clauses.
        pattern="^\s*(-?\w*)\s*<===\s*(.*)\s*$"
        causal_links_text = re.findall(pattern, text, flags=re.MULTILINE)
        
        causal_links = []

        for conseqs_text,causes_text in causal_links_text:
            
            conseqs = list(re.findall("([\w-]+)", conseqs_text))
            causes = list(re.findall("([\w-]+)", causes_text))
            causal_links.append((causes,conseqs))
            
            for cause in causes:
                predicates.add(cause)
            for conseq in conseqs:
                predicates.add(conseq)
            
        return_dict['causal_links']=causal_links
        
        # Store the preferences.
        pattern="preference\(\s*?(-?\w*)\s*?,\s*?(-?\d*)\s*?\)"
        preferences_text = re.findall(pattern, text, flags=re.MULTILINE)
        preferences = {}
        for predicat,value in preferences_text:
            preferences[predicat]=int(value)
        
        return_dict['preferences'] = preferences
        
        # Store the actions.
        pattern="action\(\s*?(\w*)\s*?\)"
        return_dict['actions'] = re.findall(pattern, text, flags=re.MULTILINE)
        
        for action in return_dict['actions']:
            predicates.add(action)
        
        # Store the defaults.   
        pattern="default\(\s*?(-?\w*)\s*?\)"
        return_dict['defaults'] = re.findall(pattern, text, flags=re.MULTILINE)
        
        # Store the initial situations.
        pattern="initial_situation\(\s*?(-?\w*)\s*?\)"
        return_dict['initial_situations'] = re.findall(pattern, text, flags=re.MULTILINE)
        
        # Store the predicate negations.
        for predicate in set(predicates):
            if predicate[0]=="-":
                predicates.add(predicate[1:])
            else:
                predicates.add("-"+predicate)
         
                
        return_dict['predicates']=predicates
        
        return return_dict
    
    @staticmethod    
    def setup_data(filename):
        """Reads the textual data and converts it into the corresponding
        Predicate objects.
        """
        
        data_dict = Preprocessor.__text_init(filename)
        predicates = {}
        logical_links = []
        for name in data_dict['predicates']:
            
            if name[0]!='-':
                negation_name = '-'+name
            else:
                negation_name = name[1:]

            if name in data_dict['preferences']:
                value =  data_dict['preferences'][name]
            elif negation_name in data_dict['preferences']:
                value =  -data_dict['preferences'][negation_name]
            else:
                value = 0
            
    
            actionable = (name in data_dict['actions']) or (negation_name in data_dict['actions'])
            
            realised =  name in data_dict['initial_situations']
    
            conceived = (name in data_dict['defaults']) or realised
    
    
            predicate = Predicate(name, value, actionable, realised, conceived)
            
            if negation_name in predicates :
                negation_predicate = predicates[negation_name]
                predicate.negation = negation_predicate
                negation_predicate.negation = predicate
          
            predicates[name] = predicate
        
        for link in data_dict['causal_links']:
            causes = [predicates[name] for name in link[0]]
            conseqs = [predicates[name] for name in link[1]]
            logical_link = Causal_link(causes,conseqs)
            logical_links.append(logical_link)
            for name in link[0]+link[1]:
                if logical_link not in predicates[name].logical_links:
                    predicates[name].logical_links.append(logical_link)
                  
        
        for name in predicates:
            if predicates[name].conceived and not predicates[name].negation.realised:
                predicates[name].realised = True          
            
        return predicates,logical_links

        


# In[4]:


"""
Created on Sat Jun 17 18:06:00 2017

@author: Tasslehoff
"""

class Predicate:
    """Represents a predicate in the extended sense, with value, causes, 
    consequences etc.
    """
    
    def __init__(self, name, value, actionable, realised, conceived): 
        self.name = name
        self.value = value
        self.actionable = actionable
        self.realised = realised
        self._init_situation = realised
        self.conceived = conceived
        self.reconsiderable = (value!=0)
        self.negation = None
        self.logical_links = []
    
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Pred_\""+self.name+"\""
    __str__ = __repr__
    #-----------------------------

    
    def is_mutable(self,N):
        """Indicates if the predicate is mutable with intensity N."""
        return N*self.value<=0 and abs(self.value)<abs(N)
        
    def is_possible(self):
        """Indicates if the predicate is possible."""
        return (not self.negation.realised) or self.actionable
    
    #def propagate_change(self):
        #"""Propagates the update of status forward in the rule set."""
        #for link in self.logical_links:
            #link.propagate_change(self)
        
    def update(self,changed_cause):
        """Updates the status according to the rules and current status of
        causes.
        """
        being_realised = False
        for link in self.logical_links:
            if link.makes_true(self):
                being_realised = True
                break
        if not self.realised and being_realised:
            print("Inferring %s from %s" %(self.name,changed_cause.name))
            self.make_true()

        elif self.realised and not being_realised and not self._init_situation:
            print("Went back to %s because of %s" %(self.negation.name,changed_cause.negation.name))
            self.negation.make_true()
        

        
    def make_action(self):
        """Makes the action corresponding to the predicate if there is one.
        (to be overwritten for particular instances of this class)
        """
        return


# In[5]:


"""
Created on Sun Jun 18 15:03:21 2017

@author: Tasslehoff
"""

class Logical_link:
    """Represents a logical link of any kind between different predicates."""
    def __init__(self, link_type):
        self.link_type = None
    
    def find_causes(self, T, N):
        """Find a cause for T if the link provides one, or None."""
        raise NotImplementedError("Please Implement this method")
        
        
    def propagate_change(self, T):
        """Propagates a change on T through the logical link."""
        raise NotImplementedError("Please Implement this method")
        
    def makes_true(self,T):
        """Checks if the logical link has predicate T as a consequence."""
        raise NotImplementedError("Please Implement this method")

        
class Causal_link(Logical_link):
    """Represents a causal link between two lists of predicates."""
    
    def __init__(self, causes, consequences, link_type):
        self.causes = causes
        self.consequences = consequences
        link_type = "causal"
    
    #-----------------------------
    # Changing the representation of the object for better readability in
    # debugging
    def __repr__(self):
        return "Logic_(%s --> %s)"%(self.causes,self.consequences)
    __str__ = __repr__
    #-----------------------------
        
    def find_causes(self, T):
        if T in self.consequences:
            return self.causes
        return None
    
    def propagate_change(self,T):
        if T in self.causes:
            for P in self.consequences:
                P.update(T)
    
    def makes_true(self, T):  
        if T in self.consequences:
            if all(P.realised for P in self.causes):
                return True
        return False


# In[6]:


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
            propagation(T)
            propagation()
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

        



# In[15]:


"""
Created on Sat Jun 17 18:24:40 2017

@author: Tasslehoff
"""

#from preprocessing import Preprocessor
#from argumenting import Argumentator
#import sys

#if __name__ == '__main__':
    #if len(sys.argv) != 2:
        #message = ("This script needs one argument : the path to the file " 
                   #"containing the predicate data.")
        #print(message)
        #sys.exit()
    #filename = sys.argv[1]
    #predicates = Preprocessor.setup_data(filename)
    #Argumentator.argue(predicates)

from preprocessing import Preprocessor
from argumenting import Argumentator
filename = "doors.pl"
predicates,logical_links = Preprocessor.setup_data(filename)
Argumentator.argue(predicates)


# In[ ]:




# In[10]:

from preprocessing import Preprocessor
from argumenting import Argumentator
filename = "doors.pl"
predicates,logical_links = Preprocessor.setup_data(filename)
Argumentator.argue(predicates)


# In[ ]:

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


# In[ ]:

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


# In[ ]:




# In[ ]:



