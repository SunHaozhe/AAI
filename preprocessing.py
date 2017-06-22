# -*- coding: utf-8 -*-
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
        incompatibility_links = []

        for conseqs_text,causes_text in causal_links_text:
            
            conseqs = list(re.findall("([\w-]+)", conseqs_text))
            causes = list(re.findall("([\w-]+)", causes_text))
            causal_links.append((causes,conseqs))
            
            for cause in causes:
                predicates.add(cause)
            for conseq in conseqs:
                predicates.add(conseq)
            
        return_dict['causal_links']=causal_links
    
        #Store the incompatibilities
        pattern="^\s*(incompatible\(\[(.*)\])"
        words = re.findall(pattern, text, flags=re.MULTILINE)
        for word_text in words:
            
            word = list(re.findall("([\w-]+)", word_text))
            incompatibility_links.append(word)
            
        return_dict['incompatibility_links']=incompatibility_links
    
    
    
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
        
        
        
        
        # Store the variable predicates.
        variable1 = []
        pattern1="\s?(-?\w+\(X,\s?\w*)\s?\)"
        words = re.findall(pattern1, text, flags=re.MULTILINE)
        for word_text in words:
                
            word = list(re.findall("([\w-]+)", word_text))
            variable1.append(word)
        return_dict['variable_predicates'] = variable1
        #est ce que ça prend en compte les prédicats (x, cste1, cste2)


        variable2 = []
        pattern2="\s?(-?\w+\(\s?\w*,\s?A)\s?\)"
        words = re.findall(pattern2, text, flags=re.MULTILINE)
        for word_text in words:
                
            word = list(re.findall("([\w-]+)", word_text))
            variable2.append(word)
        return_dict['variable_predicates'] += variable2
        
        
        
        variable3 = []
        pattern3="\s?(-?\w+\(X,\s?A)\s?\)"
        words = re.findall(pattern3, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variable3.append(word)
        return_dict['variable_predicates'] += variable3
        
        
        variableA = []
        patternA="\s?(-?\w+\(X,\s?Y)\s?\)"
        words = re.findall(patternA, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variableA.append(word)
        return_dict['variable_predicates'] += variableA
        
        
        variableB = []
        patternB="\s?(-?\w+\(_,\s?_,\s?_)\s?\)"
        words = re.findall(patternB, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variableB.append(word)
        return_dict['variable_predicates'] += variableB
        
        
        
        
        variableC = []
        patternC="\s?(-?\w+\(X,\s?A)\s?\)"
        words = re.findall(patternC, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variableC.append(word)
        return_dict['variable_predicates'] += variableC
        
        
        variableD = []
        patternD="\s?(-?w+\(Y,\s?A)\s?\)"
        words = re.findall(patternD, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variableD.append(word)
        return_dict['variable_predicates'] += variableD
        
        
        
        variableE = []
        patternE="\s?(-?\w+\(X,\s?A,\s?_)\s?\)"
        words = re.findall(patternE, text, flags=re.MULTILINE)
        for word_text in words:
                    
            word = list(re.findall("([\w-]+)", word_text))
            variableE.append(word)
        return_dict['variable_predicates'] += variableE
        
        
        
        variableF = []
        patternF="\s?(-?\w+\(X)\s?\)"
        words = re.findall(patternF, text, flags=re.MULTILINE)
        for word_text in words:
                
            word = list(re.findall("([\w-]+)", word_text))
            variableF.append(word)
        return_dict['variable_predicates'] += variableF
    
    
            
            
        
        
        
        
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
            
            nb_arguments == 0
            
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
    
            if name in data_dict['defaults']:
                default = 1
            elif negation_name in data_dict['defaults']:
                default = -1
            else:
                default = 0
                
            for i in range(0, len(return_dict['variable_predicates'])):
                if name == return_dict['variable_predicates'][i][0]:
                    nb_arguments == len(return_dict['variable_predicates'][i])
                    
                
    
            predicate = Predicate(name, value, actionable, realised, default, nb_arguments)
            predicate.set_arguments
            
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
            if predicates[name].default==1 and not predicates[name].negation.realised:
                predicates[name].realised = True          
            
        return predicates,logical_links

  """
print(return_dict['variable_predicates'])
print(logical_links)
"""      