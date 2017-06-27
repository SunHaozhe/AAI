#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Monday Jun 26 2017

@author: Haozhe Sun
"""

class Theme():
    def __init__(self, text):
        self.name = text                      #only takes 3 possible strings "doors", "tennis" and "proportional"
        self.predicates = []                  #reality status, list of strings
        self.logical_links = []               #logical links, list of strings
        self.procedureFinished = False        #if the procedure is blocked or finished, boolean
        self.consoleMessage = ""              #message displayed in the terminal console

    def getName(self):
        return self.name

    def getPredicates(self):
        return self.predicates

    def getLogicalLinks(self):
        return self.logical_links

    def procedureIsFinished(self):
        return self.procedureFinished

    def getConsoleMessage(self):
        pass

    def setProcedureFinished(self):
        self.procedureFinished = True

    def setPredicates(self, predicates):
        self.predicates = predicates

    def setLogicalLinks(self, logical_links):
        self.logical_links = logical_links

    def setConsoleMessage(self, text):
        self.consoleMessage += text

    def resetConsoleMessage(self):
        self.consoleMessage = ""

class ThemeIterator():
    def __init__(self, theme):
        self.index = 0
        self.theme = theme
        self.consoleStringList = theme.consoleMessage

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.consoleStringList):
            if self.theme.procedureIsFinished() == False:
                self.__requestForNewStrings()
                pass
            else:
                raise StopIteration("Iterator has been used up")
        else:
            self.index += 1
            return self.consoleStringList[self.index - 1]

    def __requestForNewStrings(self):
        """ask for new strings when the procedure is waiting for user's input"""
        pass






