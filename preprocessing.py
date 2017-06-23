# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:23:18 2017

@author: Justin
"""

import re
from predicate import Predicate
from logical import Causal_link,Incompatibility_link

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
        
        # Store the causal clauses.
        pattern="^\s*(-?\w*)\s*<===\s*(.*)\s*$"
        causal_links_text = re.findall(pattern, text, flags=re.MULTILINE)
        
        causal_links = []
        incompatibility_links = []

        for conseq_text,causes_text in causal_links_text:
            
            conseq = list(re.findall("([\w-]+)", conseq_text))[0]
            causes = list(re.findall("([\w-]+)", causes_text))
            causal_links.append((causes,conseq))
            
            for cause in causes:
                predicates.add(cause)
            predicates.add(conseq)
    
        return_dict['causal_links']=causal_links
        
        
        #Store the incompatibilities
        pattern="^\s*incompatible\(\[(.*)\]"
        incompatibility_list_texts = re.findall(pattern, text, flags=re.MULTILINE)
        for incompatibility_text in incompatibility_list_texts:
            
            incompatibility = list(re.findall("([\w-]+)", incompatibility_text))
            incompatibility_links.append(incompatibility)
            for pred in incompatibility:
                predicates.add(pred)
            
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
        return_dict['initial_situations'] = list(re.findall(pattern, text, flags=re.MULTILINE))
        
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
            

    
            if name in data_dict['defaults']:
                default = 1
            elif negation_name in data_dict['defaults']:
                default = -1
            else:
                default = 0
            
            
            if name[0]=='-' and (name not in data_dict['initial_situations']):
                if negation_name not in data_dict['initial_situations'] and default>=0:
                    data_dict['initial_situations'].append(name)
            
    
            realised = name in data_dict['initial_situations']
                
            predicate = Predicate(name, value, actionable, realised, default)
            
            if negation_name in predicates :
                negation_predicate = predicates[negation_name]
                predicate.negation = negation_predicate
                negation_predicate.negation = predicate
          
            predicates[name] = predicate
        
        for link in data_dict['causal_links']:
            causes = [predicates[name] for name in link[0]]
            conseq = predicates[link[1]]
            logical_link = Causal_link(causes,conseq)
            logical_links.append(logical_link)
            
        for incompatibilities in data_dict['incompatibility_links']:
            incompatibilities = [predicates[name] for name in incompatibilities]
            logical_link = Incompatibility_link(incompatibilities)
            logical_links.append(logical_link)
            
            
        return predicates, logical_links, data_dict["initial_situations"]

        