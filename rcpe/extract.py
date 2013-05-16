#!/bin/python
# -*- coding: utf-8 -*-

import mydb
import json
import re
from nltk.stem.wordnet import WordNetLemmatizer
from stanford_parser import parser
import json

# parsers
sp = parser.Parser()
wnl = WordNetLemmatizer()


def search(array,rel,gov,dep):
    for e in array:
        if e[0] == rel and (gov==None and True or gov==e[1]) and (dep==None and True or dep ==e[2]):
            return e


def toPhrase(clause,sp,l):
    '''
    convert the clause into phrase
    sp: stanford parser
    l : wordnet lemmatizer 
    '''
    print
    print 'clause:',clause
    print

    phrase = {'subj':None,'subj_adj':None,
              'verb':None,'adv':None,'neg':False,
              'dobj':None,'dobj_adj':None,
              'iobj':None,'iobj_adj':None}

    dep = None
    try:
        dep = sp.parseToStanfordDependencies(clause)
    except AssertionError,e:
        return phrase
    dependencies = dep.dependencies
    
    tsfmap = {}
    tokens = dep.tokens
    posTags = dep.posTags
    for i in xrange(len(tokens)):
        tsfmap[tokens[i]]=i
    
    triples = [(rel, gov.text+'_'+str(tsfmap[gov]), dep.text+'_'+str(tsfmap[dep])) 
               for rel, gov, dep in dependencies]
    for r in triples:
        print r
    
    
    # search for nsubj: get the sub and verb, get the first
    e = search(triples,'nsubj',None,None)
    if e:
        phrase['subj'] = e[2]
        phrase['verb'] = e[1]
        
        # search for subj_adj:
        e5 = search(triples,'amod',e[2],None)
        if e5:
            phrase['subj_adj'] = e5[2]
        
        # search for 'cop'
        e6 = search (triples,'cop',e[1],None)
        if e6:
            phrase['verb'] = e6[2]
            phrase['dobj']= e[1]
        # search for advmod: get the adv
        e1 = search(triples,'advmod',e[1],None)
        if e1:
            phrase['adv'] = e1[2]

        # search for dobj: get the dobj
        e2 = search(triples,'dobj',e[1],None)
        if e2:
            phrase['dobj']=e2[2]
        e21 = search(triples,'amod',phrase['dobj'],None)
        if e21:
            phrase['dobj_adj'] = e21[2]

        # search for iojb: get the iobj
        e3 = search(triples,'iobj',e[1],None)
        if e3:
            phrase['iobj']=e3[2]
            e31 = search(triples,'amod',e3[2],None)
            if e31:
                phrase['iobj_adj'] = e31[2]

        # search for neg
        e4 = search(triples,'neg',e[1],None)
        if e4:
            phrase['neg']=True

    # stem the verbs and words 
    
    # verb:
    if phrase['verb'] != None:
        suffix = phrase['verb'][-2:]
        word = l.lemmatize(phrase['verb'][:-2],'v')
        phrase['verb'] = word+suffix
    
    # nouns:
    attrs = ['subj','dobj','iobj']
    for attr in attrs:
        if phrase[attr] != None:
            suffix = phrase[attr][-2:]
            word = l.lemmatize(phrase[attr][:-2],'n')
            phrase[attr] = word+suffix
   
    print phrase
    return phrase

def engine(clauses, query):
    '''
    query 'C R+^because R^and'
    query 'C R^because_/p'\
    + means first letter inital
    '''
    pairs=[]
    prefixs = []
    suffixs = []
    initals = []
    rcs = []
    qs = query.split(' ')
    for q in qs:
        s = (q+'_').index('_')
        if s != len(q):
            suffixs.append(q[s+1:])
            q = q[:s]
        else:
            suffixs.append('')
        qq = (q+'^').index('^')
        if qq != len(q):
            prefixs.append(q[qq+1:])
            q = q[:qq]
        else:
            prefixs.append('')
        if '+' in q:
            initals.append('+')
            q = q[0]
        else:
            initals.append('')
        rcs.append(q)
    

    for i in xrange(len(clauses)-len(qs)+1):
        match = True
        # check for prefix
        for j in xrange(len(qs)):
            if prefixs[j] == '':
                continue
            else:
                clause = clauses[i+j]
                if (prefixs[j]+' ').lower() != clause[:len(prefixs[j])+1].lower():
                    match = False
                    break
        # check for initals
        for j in xrange(len(qs)):
            if initals[j]=='':
                continue
            else:
                clause = clauses[i+j]
                if len(clause) == 0 or clause[0] == clause[0].lower():
                    match = False
                    break
        # check for suffix
        for j in xrange(len(qs)):
            if suffixs[j] == '':
                continue
            else:
                clause = clauses[i+j]
                words = clause.split()
                if suffixs[j] == r'/p':
                    if len(words)==0 or words[-1] not in ['.',',','!']:
                        match = False
                        break
                else:
                    if len(words)==0 or (suffixs[j].startswith('<>') and words[-1] == suffixs[j][2:]):
                        match = False
                        break
                    elif (not suffixs[j].startswith('<>')) and words[-1] != suffixs[j]:
                        match = False
                        break
        if match:
            reasons = []
            consequences = [] 
            for j in xrange(len(rcs)):
                if rcs[j] == 'O':
                    continue
                elif rcs[j] == 'R':
                    reasons.append((clauses[i+j],i+j))
                elif rcs[j] == 'C':
                    consequences.append((clauses[i+j],i+j))
            pairs.append((reasons,consequences))
    return pairs


def processReview(clauses,sp,wnl):
    pairs = []

    temp_pairs = engine(clauses,'C+ R^because_<>. R^and_/p')
    m = {}
    for t in temp_pairs:
        for c in t[0]+t[1]:
          m[c[1]] = 1  

    temp_pairs2 = engine(clauses,'C+ R^because_/p')
    for t in temp_pairs2:
        ist = True
        for c in t[0]+t[1]:
            if c[1] in m:
                ist=False
                break
        if ist:
            temp_pairs.append(t)

    for tpair in temp_pairs:
        treasons = tpair[0]
        tconsequences = tpair[1]
        reasons = []
        consequences = []
        for treason in treasons:
            phrase = toPhrase(treason[0],sp,wnl)
            reasons.append((phrase,treason[1]))
        for tconsequence in tconsequences:
            phrase = toPhrase(tconsequence[0],sp,wnl)
            consequences.append((phrase,tconsequence[1]))
        pairs.append((reasons,consequences))
    return temp_pairs,pairs


def main():
    # file to save
    jfile = open('result.tuple.json.txt','w')
    jsfile = open('result.sentence.json.txt','w')
    file = open('result.txt','w')
    jhfile = open('result.jh.txt','w')
    # db
    CONN_STRING = mydb.get_CONN('wiki')
    con = mydb.getCon(CONN_STRING)
    query = 'select id , review_clauses from review order by id limit 1000'
    rows = mydb.executeQueryResult(con,query,True)
    
    for row in rows:
        id = row[0]
        review = row[1]
        if not review:
            continue
        review = review.decode('utf-8')
        clauses = review.split('###')
        tpairs,pairs = processReview(clauses,sp,wnl)
        if len(pairs) == 0:
            continue
        jfile.write(json.dumps({'id':id,'pairs':pairs})+'\n')
        jsfile.write(json.dumps({'id':id,'sen_pairs':tpairs})+'\n')
        
        file.write('id:'+str(id)+'\n')
        jhfile.write('id:'+str(id)+'\n')
        for tpair in tpairs:
            file.write('Reasons:'+repr(tpair[0])+'\n')
            file.write('Consequences:'+ repr(tpair[1])+'\n')
            
        for pair in pairs:
            jhfile.write('Reasons:\n')
            jhfile.write(repr(pair[0][0][0]['subj'])+' ')
            jhfile.write(repr(pair[0][0][0]['verb'])+' ')
            jhfile.write(repr(pair[0][0][0]['dobj'])+' ')
            jhfile.write(repr(pair[0][0][0]['iobj'])+'\n')
            
            jhfile.write('Consequences:\n')
            jhfile.write(repr(pair[1][0][0]['subj'])+' ')
            jhfile.write(repr(pair[1][0][0]['verb'])+' ')
            jhfile.write(repr(pair[1][0][0]['dobj'])+' ')
            jhfile.write(repr(pair[1][0][0]['iobj'])+'\n')
            
    file.close()
    jfile.close()
    jhfile.close()

if __name__ == '__main__':
    main()
