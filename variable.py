# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:10:40 2017

@author: Guerric
"""


import re
with open("tennis2.pl") as file:
    text=file.read()

return_dict = {}

# Store the variable predicates.
variable1 = []
pattern1="\s?(-?\w+\(X,\s?\w*)\s?\)"
words = re.findall(pattern1, text, flags=re.MULTILINE)
for word_text in words:
            
    word = list(re.findall("([\w-]+)", word_text))
    variable1.append(word)
return_dict['variable_predicates'] = variable1
#est ce que ça prend en compte les prédicats (x, cste1, cste2)
"""
pattern0= "\((\w*)\)"
return_dict['variable_predicates'] += list(re.findall(pattern0, text, flags=re.MULTILINE))
"""


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





instanciation_predicate = []
for predicate in return_dict['predicate']:
    instanciation = [predicate]


for predicate in return_dict['predicates']:
    m=0
    pattern5="^[^\(]*)\("
    p=re.search(pattern5,predicate).group(0)
    for i in range(0, len(return_dict['variable_predicates'])):
        if p == re.search(pattern5, return_dict['variable_predicates'][i]).group(0):
            m=i
    
    attributes = list(re.findall("([\w-]+)", predicate))
    
    first_attribute= attributes[0]
    instanciation_predicate_m[0].add(first_attribute)
    
    second_attribute= attributes[1]
    instanciation_predicate_m[1].add(second_attribute)
    
    
    third_attribute= attributes[1]
    instanciation_predicate_m[2].add(third_attribute)


"""
In [17]:
import re
pattern1="joue"
re.findall(pattern1, text, flags=re.MULTILINE)
Out[17]:
[]
In [20]:
print(return_dict['variable_predicates'])
[]
In [ ]:
"""