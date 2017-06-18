# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:23:18 2017

@author: Justin
"""

import re
from predicate import Predicate

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
        clauses_text = re.findall(pattern, text, flags=re.MULTILINE)
        clauses = {}
            
        for conseq,causes in clauses_text:
            if conseq in clauses:
                clauses[conseq] += [re.findall("([\w-]+)", causes)]
            else:
                clauses[conseq] = [re.findall("([\w-]+)", causes)]
            predicates.add(conseq)
            for cause_list in clauses[conseq]:
                for cause in cause_list:
                    predicates.add(cause)         
            
        return_dict['clauses']=clauses
        
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
        for name in data_dict['predicates']:
            
            if name in data_dict['preferences']:
                value =  data_dict['preferences'][name]
            else:
                value = 0
            
            if name[0]!='-':
                negation_name = '-'+name
            else:
                negation_name = name[1:]
    
            actionable = name in data_dict['actions'] or negation_name in data_dict['actions']
            
            realised =  name in data_dict['initial_situations']
    
            conceived = name in data_dict['defaults'] or realised
    
    
            predicate = Predicate(name, value, actionable, realised, conceived)
            
            if negation_name in predicates :
                negation_predicate = predicates[negation_name]
                predicate.negation = negation_predicate
                negation_predicate.negation = predicate
          
            predicates[name] = predicate
    
        for name in predicates:
            if predicates[name].conceived and not predicates[name].negation.realised:
                predicates[name].realised = True
            if name in data_dict['clauses']:
                cause_lists = data_dict['clauses'][name]
                for cause_list in cause_lists:
                    cause_tuple = tuple(predicates[pred_name] for pred_name in cause_list)
                    predicates[name].cause_tuples.add(cause_tuple)
                    for cause in cause_tuple:
                        cause.consequences.add(predicates[name])
            else:
                cause_lists = []
            
            for cause_tuple in predicates[name].cause_tuples:
                for cause in cause_tuple:
                    cause.consequences.add(predicates[name])
        return predicates

        