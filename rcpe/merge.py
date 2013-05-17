#!/usr/bin/python
# -*- coding: utf-8 -*-

# merge.py
#
# to merge the results of SPADE parseing and coref analysis
#
# Usage: python getConse.py -u username -f file
# username - the username of DB
# file - the path to input file
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


def merge(file):
    con = mydb.getCon(CONN_STRING)
    #iter = 1
    json_date = open(file)
    map = {}
    totalRepl = 0
    totalReplDone = 0
          
    for entry in json_date:
        data = json.loads(entry)
        query = "select id, review_clauses from review where id = '" + data['id'] + "'"
        corefStr = data['review_text']
        resultSet = mydb.executeQueryResult(con, query, False)
        #clauseStr = ''.join(resultSet[1])
        
        if resultSet[0][1] == None:
            continue
        clauseStr = resultSet[0][1].decode('utf-8')
        clauseStr = re.sub(r"(\.+)", ".", clauseStr)
        corefStr = corefStr.replace("-RRB-", ")").replace("-LRB-", "(")
        corefStr = re.sub(r"(\.)+", ".", corefStr)
        corefLst = corefStr.split()
        i = 0
        corefLst_2 = []
        
        while i < len(corefLst):
            if "<--" in corefLst[i]:
                totalRepl += 1
                str = ''
                j = i
                while not corefLst[j].endswith("-->"):
                    str += corefLst[j] + ' '
                    j += 1
                    #print str
                #if j == i:
                str += corefLst[j]
                corefLst_2.append(str)
                i = j
            else:
                corefLst_2.append(corefLst[i])
            i += 1
        clauseLst = clauseStr.split()
        clauseLstClone = list(clauseLst)
        loc_clause = 0
        loc_coref = 0

        while loc_coref < len(corefLst_2):
            resCorefWord = getCorefWord(loc_coref, corefLst_2)
            if resCorefWord[0]:
                match = False
                word_coref = resCorefWord[1]
                loc_clause_cur = loc_clause
                while loc_clause_cur < len(clauseLst):                   
                    word_clause = getClauseWord(loc_clause_cur, clauseLst)
                    
                    if word_clause == word_coref:
                        i = 1
                        prevMatch = False
                        prevClause = ''
                        prevCoref = ''
                        
                        while loc_clause_cur - i >= 0 and i <= 3 and loc_coref - i >= 0:
                            prevCoref = getCorefWord(loc_coref-i,corefLst_2)[1] + prevCoref
                            prevClause = getClauseWord(loc_clause_cur-i,clauseLst) + prevClause
                            i += 1
                        prevClause = prevClause.replace("`", "'")
                        prevCoref= prevCoref.replace("`", "'")
                        prevCoref= prevCoref.replace("\/", "/")
                        if prevCoref.endswith(prevClause) or prevClause.endswith(prevCoref) or prevCoref.startswith(prevClause) or prevClause.startswith(prevCoref):
                            prevMatch = True
                        i = 1
                        nextMatch = False
                        nextClause = ''
                        nextCoref = ''
                        while loc_clause_cur + i < len(clauseLst) and i <= 3 and loc_coref + i < len(corefLst_2):
                            nextCoref = nextCoref + getCorefWord(loc_coref+i,corefLst_2)[1]
                            nextClause = nextClause + getClauseWord(loc_clause_cur+i,clauseLst)
                            i += 1
                        nextClause = nextClause.replace("`", "'")
                        nextCoref = nextCoref.replace("`", "'")
                        nextCoref = nextCoref.replace("\/", "/")
                        if nextClause.startswith(nextCoref) or nextCoref.startswith(nextClause) or nextClause.endswith(nextCoref) or nextCoref.endswith(nextClause):
                            nextMatch = True
                        if prevMatch and nextMatch:
                            repl = corefLst_2[loc_coref][corefLst_2[loc_coref].index("<--"):corefLst_2[loc_coref].index("-->")+3]
                            match = match or True
                            totalReplDone += 1
                            clauseLstClone[loc_clause_cur] += repl
                    loc_clause_cur += 1
            loc_coref += 1
            loc_clause += 1
        map[int(data['id'])] = genJSON(clauseLstClone)
    print totalReplDone, totalRepl, (totalReplDone + 0.0)/totalRepl
    with open('data.txt', 'w') as outfile:
        json.dump(map, outfile)


def genJSON(clauseLstClone):
    clauseLst = ' '.join(clauseLstClone).split("###")
    k = 0
    bigMap = {}
    while k < len(clauseLst):
        map = {}
        clauseLstClone = clauseLst[k].split()
        i = 0
        r = 0
        while i < len(clauseLstClone):
            if "<--" in clauseLstClone[i]:
                s = ''
                j = i
                while not clauseLstClone[j].endswith("-->"):
                    s += clauseLstClone[j] + ' '
                    j += 1
                s += clauseLstClone[j]
                s = s[s.index("<--"):s.index("-->")+3]
                #print str
                map[r] = s.encode('utf-8',errors = 'ignore')
                #print type(map[r])
                #print str
                i = j
            i += 1
            r += 1
        if not len(map.keys()) == 0:
            bigMap[k] = map
        k += 1
    return bigMap

def getCorefWord(loc_coref, corefLst_2):
    token = corefLst_2[loc_coref]
    if token.endswith("-->"):
        word_coref = token[0:token.index('<--')]
        return (True, word_coref)
    return (False, token)
        

def getClauseWord(loc_clause_cur, clauseLst):
    word_clause = clauseLst[loc_clause_cur]
    if word_clause.endswith('###'):
        word_clause = clauseLst[loc_clause_cur][0 : clauseLst[loc_clause_cur].index('###')]
    elif word_clause.startswith('###'):
        word_clause = clauseLst[loc_clause_cur][clauseLst[loc_clause_cur].index('###')+3 : ]
    else:
        word_clause = clauseLst[loc_clause_cur]
    return word_clause


if __name__ == '__main__':
    from optparse import OptionParser
   	
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-u",'--user',dest='username',help='username')
    parser.add_option("-f","--file",dest ='file', help="input file")
    (options,args) = parser.parse_args()
    username = options.username
    file = options.file
    
    CONN_STRING = mydb.get_CONN(username)
    merge(file)

    
