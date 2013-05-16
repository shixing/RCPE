import mydb
import json
from pprint import pprint
import psycopg2
import nltk
import os
import re

def merge(iter):
    con = mydb.getCon(CONN_STRING)
    #iter = 1
    json_date = open('./coref/reviewCoref' + iter +'.json.txt')
    map = {}
    totalRepl = 0
    totalReplDone = 0        
    for entry in json_date:
        data = json.loads(entry)
        #if int(data['id']) >= 10:
            #break
        query = "select id, review_clauses from review where id = '" + data['id'] + "'"
        corefStr = data['review_text']
        resultSet = mydb.executeQueryResult(con, query, False)
        #print resultSet
        #clauseStr = ''.join(resultSet[1])
        if resultSet[0][1] == None:
            continue
        clauseStr = resultSet[0][1].decode('utf-8')
        
        clauseStr = re.sub(r"(\.+)", ".", clauseStr)
        #print clauseStr
        corefStr = corefStr.replace("-RRB-", ")").replace("-LRB-", "(")
        corefStr = re.sub(r"(\.)+", ".", corefStr)
        corefLst = corefStr.split()
        i = 0
        corefLst_2 = []
        #print corefStr
        #print corefLst
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
        #print corefLst_2
        loc_clause = 0
        loc_coref = 0
        #for token in corefLst_2:
        while loc_coref < len(corefLst_2):
            #token = corefLst_2[loc_coref]
            resCorefWord = getCorefWord(loc_coref, corefLst_2)
            #if token.endswith("-->"):
            #print data['id']
            #print resCorefWord,
            if resCorefWord[0]:
                match = False
                #print resCorefWord
                #word_coref = token[0:token.index('<--')]
                word_coref = resCorefWord[1]
                loc_clause_cur = loc_clause
                while loc_clause_cur < len(clauseLst):                   
                    word_clause = getClauseWord(loc_clause_cur, clauseLst)
                    #print word_clause
                    #if word_clause.endswith('###'):
                    #    word_clause = clauseLst[loc_clause_cur][0 : clauseLst[loc_clause_cur].index('###')]
                    #elif word_clause.startswith('###'):
                    #    word_clause = clauseLst[loc_clause_cur][clauseLst[loc_clause_cur].index('###') +1 : ]
                    #else:
                    #    word_clause = clauseLst[loc_clause_cur]
                    
                    #print word_clause, word_coref,
                    if word_clause == word_coref:
                        #print word_clause, word_coref
                        i = 1
                        prevMatch = False
                        prevClause = ''
                        prevCoref = ''
                        while loc_clause_cur - i >= 0 and i <= 3 and loc_coref - i >= 0:
                            #print getClauseWord(loc_clause_cur-i, clauseLst), getCorefWord(loc_coref-i, corefLst_2)[1]
                            #prevMatch=prevMatch and getCorefWord(loc_coref-i,corefLst_2)[1].startswith(getClauseWord(loc_clause_cur-i,clauseLst))
                            prevCoref = getCorefWord(loc_coref-i,corefLst_2)[1] + prevCoref
                            prevClause = getClauseWord(loc_clause_cur-i,clauseLst) + prevClause
                            i += 1
                        prevClause = prevClause.replace("`", "'")
                        prevCoref= prevCoref.replace("`", "'")
                        prevCoref= prevCoref.replace("\/", "/")
                        #print data['id'] , prevCoref , prevClause
                        if prevCoref.endswith(prevClause) or prevClause.endswith(prevCoref) or prevCoref.startswith(prevClause) or prevClause.startswith(prevCoref):
                            prevMatch = True
                            #print prevMatch
                        i = 1
                        nextMatch = False
                        nextClause = ''
                        nextCoref = ''
                        while loc_clause_cur + i < len(clauseLst) and i <= 3 and loc_coref + i < len(corefLst_2):
                            #print getClauseWord(loc_clause_cur+i, clauseLst),getCorefWord(loc_coref+i, corefLst_2)[1]
                            #nextMatch=nextMatch and getCorefWord(loc_coref+i,corefLst_2)[1].startswith(getClauseWord(loc_clause_cur+i,clauseLst))
                            nextCoref = nextCoref + getCorefWord(loc_coref+i,corefLst_2)[1]
                            nextClause = nextClause + getClauseWord(loc_clause_cur+i,clauseLst)
                            i += 1
                        nextClause = nextClause.replace("`", "'")
                        nextCoref = nextCoref.replace("`", "'")
                        nextCoref = nextCoref.replace("\/", "/")
                        #print data['id'] , nextCoref , nextClause
                        if nextClause.startswith(nextCoref) or nextCoref.startswith(nextClause) or nextClause.endswith(nextCoref) or nextCoref.endswith(nextClause):
                            nextMatch = True
                            #print nextMatch
                        if prevMatch and nextMatch:
                            repl = corefLst_2[loc_coref][corefLst_2[loc_coref].index("<--"):corefLst_2[loc_coref].index("-->")+3]
                            #print corefLst_2[loc_coref], repl
                            match = match or True
                            totalReplDone += 1
                            clauseLstClone[loc_clause_cur] += repl
                            
                    loc_clause_cur += 1
                #if not match:
                    #print data['id'], corefLst_2[loc_coref], corefLst_2[loc_coref -1 ]
            loc_coref += 1
            loc_clause += 1
        map[int(data['id'])] = genJSON(clauseLstClone)
        if int(data['id']) % (50 + int(i))  == 0:
            print int(data['id'])
    print totalReplDone, totalRepl, (totalReplDone + 0.0)/totalRepl
    #print '\n'.join((' '.join(clauseLstClone).split("###")))
    print map
    #f = open('data2.txt', 'w')
    #for key in map:
    #    f.write(''.join(str(map[key])))
    #    f.write('\n')
    #f.close()
    with open('data' + iter +'.3.txt', 'w') as outfile:
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
        #print token
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
    CONN_STRING = mydb.get_CONN('xingshi')
    for i in range(0,4):
        merge(str(i))

    
