#!/usr/bin/python
# -*- coding: utf-8 -*-

# rcCoref.py
#
# to a replacing map that indicates which words should be replaced according to coref
# format of input file:
# {"sen_pairs": [[[["because I 've heard so many good things about this place . ", 36]], [["It 's odd , ", 35]]]], "id": 54235}
# format of output file:
# {"coref": {"<--a great way to wind down on a warm Friday night-->": {"14": [0, 1], "15": [1, 1]}}, "id": 50}
#
# Usage: python reaconMap.py -u username -i input -o output
# username - username of DB
# input - path to input file
# output - path to output file
#
# Author: Ai He
# contact: aihe@usc.edu

import mydb
import json
from pprint import pprint
import psycopg2
import nltk
import os
import re
import ast


def rcCoref(input, output):
    con = mydb.getCon(CONN_STRING)
    json_date = open(input)
    total = 0
    bMap = {}
    
    for entry in json_date:
        total += 1
        data = json.loads(entry)
        iden = int(data['id'])
        query = "select replace from coref  where id = '" + str(data['id']) + "'"
        resultSet = mydb.executeQueryResult(con, query, False)
        if len(resultSet) == 0:
            continue
        repl = json.loads(resultSet[0][0])
        reacons = data['sen_pairs']
        sMap = {}
        
        for reacon in reacons:
            reas = reacon[0]
            cons = reacon[1]
            reaMap = {}
            consMap = {}
            iRea = 0
            for rea in reas:
                if str(rea[1]) in repl:
                    rep = repl[str(rea[1])]             
                    for key in rep:                
                        if not rep[key] in reaMap:
                            reaMap[rep[key]] = {rea[1]: (int(key),1)}
                        else:                            
                            if rea[1] in reaMap[rep[key]]:                                
                                reaMap[rep[key]][rea[1]] = (min(reaMap[rep[key]][rea[1]][0], int(key)), reaMap[rep[key]][rea[1]][1] + 1)                                
                            else:
                                reaMap[rep[key]][rea[1]] = (int(key), 1)
                                
            for cons in cons:
                if str(cons[1]) in repl:
                    rep = repl[str(cons[1])]                    
                    for key in rep:                
                        if not rep[key] in consMap:
                            consMap[rep[key]] = {cons[1]: (int(key),1)}
                        else:
                            if cons[1] in consMap[rep[key]]:
                                consMap[rep[key]][cons[1]] = (min(consMap[rep[key]][cons[1]][0], int(key)), consMap[rep[key]][cons[1]][1] + 1)
                            else:
                                consMap[rep[key]][cons[1]] = (int(key), 1)
                                
            for key in reaMap:
                if key in consMap:
                    for clause in reaMap[key]:
                        if not key in sMap:
                            sMap[key] = {}
                        sMap[key][clause] = reaMap[key][clause]
                    for clause in consMap[key]:
                        sMap[key][clause] = consMap[key][clause]
                        
            if not len(sMap) == 0:
                bMap[iden] = sMap
                
    outputRes(bMap, output)


def outputRes(bMap):
    f = open(output, 'w')
    lst = list(bMap.keys())
    lst.sort()
    for i in lst:
        map = {}
        map['id'] = i
        #coref = json.dumps(bMap[i])
        coref = bMap[i]
        map['coref']=coref
        f.write(json.dumps(map) + '\n')
    f.close()
        



if __name__ == '__main__':
	from optparse import OptionParser
   	
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-u","--user",dest ='username', help="username of DB")
    parser.add_option("-i","--input",dest ='input', help="path to input file")
    parser.add_option("-o","--output",dest ='output', help="path to out file")
    (options,args) = parser.parse_args()
    username = options.user
    input = options.input
    output = options.output
    
    CONN_STRING = mydb.get_CONN(username)
    rcCoref(input, output)
