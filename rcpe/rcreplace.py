#!/usr/bin/python
# -*- coding: utf-8 -*-

# rcReplace.py
#
# to replace words in reasons and consequences into coref
# format of input:
# 1. [[[["because I \'ve always wanted to do something like this ", 2], ["and thought it to be a great gift for my other half . ", 3]], [["I had purchased an online deal ", 1]]]]
# 2. {"<--a great gift for my other half-->": {"1": [3, 3], "3": [2, 1]}, "<--I-->": {"1": [0, 1], "2": [1, 1], "3": [9, 1]}}
#
# Usage: function mergeCoref is going to be called by evaluate.py
#
# Author: Ai He
# contact: aihe@usc.edu

import json


def mergeCoref(rcs, coref):
    result = []
    
    for rc in rcs:
        rMap = {}
        cMap = {}
        rs = rc[0]
        cs = rc[1]
        for r in rs:
            rMap[int(r[1])] = r[0]
        for c in cs:
            cMap[int(c[1])] = c[0]
        corefNum = 1
        
        for key in coref:
            valid = False
            clauseMap = coref[key]
            for cls in clauseMap:
                if int(cls) in rMap:
                    valid = True
                    lst = rMap[int(cls)].split()                
                    lst[int(clauseMap[cls][0])] = "#" + str(corefNum)
                    for i in range(int(clauseMap[cls][0]) + 1, int(clauseMap[cls][0]) + int(clauseMap[cls][1])):
                        lst[i] = ''
                    st = ' '.join(lst)                
                    rMap[int(cls)] = st
                    
                if int(cls) in cMap:
                    valid = True
                    lst = cMap[int(cls)].split()
                    lst[int(clauseMap[cls][0])] = "#" + str(corefNum)
                    for i in range(int(clauseMap[cls][0]) + 1, int(clauseMap[cls][0]) + int(clauseMap[cls][1])):
                        lst[i] = ''
                    st = ' '.join(lst)                
                    cMap[int(cls)] = st
                    
            if valid:
                corefNum += 1

        result.append(outputMap(rMap, cMap))
    print result


def outputMap(rMap, cMap):
    l1 = []
    l2 = []
    for k in rMap:
        l1.append(rMap[k])
    for k in cMap:
        l2.append(cMap[k])
    return (l1, l2)

if __name__ == '__main__':
    rc = '[[[["because I \'ve always wanted to do something like this ", 2], ["and thought it to be a great gift for my other half . ", 3]], [["I had purchased an online deal ", 1]]]]'
    coref = '{"<--a great gift for my other half-->": {"1": [3, 3], "3": [2, 1]}, "<--I-->": {"1": [0, 1], "2": [1, 1], "3": [9, 1]}}'
    mergeCoref(json.loads(rc), json.loads(coref))
