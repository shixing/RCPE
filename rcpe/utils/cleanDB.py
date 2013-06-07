#!/bin/python
# -*- coding: utf-8 -*-

# cleanDB.py 
# The table 'review' ' 'review_clauses' may contains clauses result which is not matched with 'review', clean it. 
# 
#
# Author: Xing Shi
# contact: xingshi@usc.edu

from rcpe import mydb
import nltk
import re

def n_gram(n,sent):
    result = []
    for i in xrange(len(sent)-n+1):
        result.append('_'.join([sent[i+k] for k in xrange(n)]))
    if len(sent) < n:
        result.append('_'.join(sent))
    return result


def jaccard_distance(sent1,sent2):
    pattern = r'[^a-zA-Z0-9]'
    sent1 = re.sub(pattern,' ',sent1)
    sent2 = re.sub(pattern,' ',sent2)
    s1 = set(n_gram(2,sent1.split()))
    s2 = set(n_gram(2,sent2.split()))
    
    if len(s2)==0:
        return (s1,s2,-1)
    else:
        return (s1,s2,len(s1.intersection(s2))*1.0/len(s2))

def clean_review_clauses():
    CONN_STRING = mydb.get_CONN()
    con = mydb.getCon(CONN_STRING)
    query = 'select id,review_text,review_clauses from review where review_clauses is not null'
    records = mydb.executeQueryResult(con,query,False)
    idxs = []
    for record in records:
        idx = record[0]
        review_text = record[1]
        review_clauses = record[2]
        review_clauses = review_clauses.replace('###','')
        s1,s2,jd=jaccard_distance(review_text,review_clauses)
        if jd<0.6: # we think this would be a bad one
            print jd,idx
            idxs.append(idx)
    
    query = 'update review set review_clauses = NULL where id = __idx__'
    for idx in idxs:
        query_n = query.replace('__idx__',str(idx))
        mydb.executeQuery(con,query_n,False)
    

if __name__ == '__main__':
    clean_review_clauses()
