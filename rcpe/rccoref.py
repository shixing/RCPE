import mydb
import json
from pprint import pprint
import psycopg2
import nltk
import os
import re
import ast

def rcCoref():
    con = mydb.getCon(CONN_STRING)
    json_date = open('result.sentence.json.txt')
    total = 0
    #bigMap = json.load(open('data0.3.txt'))
    #bigMapList = [json.load(open('data1.3.txt')), json.load(open('data2.3.txt')),json.load(open('data3.3.txt'))]
    #for b in bigMapList:
    #    for key in b:
    #        bigMap[key] = b[key]
    #print len(bigMap)
    bMap = {}
    for entry in json_date:
        #if total > 1000:
        #    break
        total += 1
        data = json.loads(entry)
        iden = int(data['id'])
        #if not iden == 559:
        #    continue
        query = "select replace from coref  where id = '" + str(data['id']) + "'"
        resultSet = mydb.executeQueryResult(con, query, False)
        #print resultSet[0][0]
        if len(resultSet) == 0:
            continue
        repl = json.loads(resultSet[0][0])
        #print repl
        #repl = resultSet
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
                        #print key, rep[key]
                        if not rep[key] in reaMap:
                            reaMap[rep[key]] = {rea[1]: (int(key),1)}
                        else:                            
                            if rea[1] in reaMap[rep[key]]:                                
                                reaMap[rep[key]][rea[1]] = (min(reaMap[rep[key]][rea[1]][0], int(key)), reaMap[rep[key]][rea[1]][1] + 1)                                
                            else:
                                reaMap[rep[key]][rea[1]] = (int(key), 1)
            #print reaMap
            for cons in cons:
                if str(cons[1]) in repl:
                    rep = repl[str(cons[1])]                    
                    for key in rep:                
                        #print key, rep[key]
                        if not rep[key] in consMap:
                            consMap[rep[key]] = {cons[1]: (int(key),1)}
                        else:
                            if cons[1] in consMap[rep[key]]:
                                consMap[rep[key]][cons[1]] = (min(consMap[rep[key]][cons[1]][0], int(key)), consMap[rep[key]][cons[1]][1] + 1)
                            else:
                                consMap[rep[key]][cons[1]] = (int(key), 1)
            #print reaMap
            #print consMap
            for key in reaMap:
                if key in consMap:
                    for clause in reaMap[key]:
                        if not key in sMap:
                            sMap[key] = {}
                        sMap[key][clause] = reaMap[key][clause]
                        #print key, clause
                        #print map[key]
                    for clause in consMap[key]:
                        #print key in map
                        #print clause in sMap[key]
                        sMap[key][clause] = consMap[key][clause]
                        
            #print len(sMap)
            if not len(sMap) == 0:
                bMap[iden] = sMap
            
    #print bMap
    outputRes(bMap)

def outputRes(bMap):
    f = open('result.coref.json.txt', 'w')
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
    CONN_STRING = mydb.get_CONN('wiki')
    rcCoref()
