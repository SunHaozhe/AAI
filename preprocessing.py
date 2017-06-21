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
    
            if name in data_dict['defaults']:
                default = 1
            elif negation_name in data_dict['defaults']:
                default = -1
            else:
                default = 0
    
    
            predicate = Predicate(name, value, actionable, realised, default)
            
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

        