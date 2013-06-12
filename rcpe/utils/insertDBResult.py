#!/bin/python
# -*- coding: utf-8 -*-

# insertDBResult.py 
# Read three files: result.[sentence/tuple/coref].json.txt, insert these result into table rc
#
# Author: Xing Shi
# contact: xingshi@usc.edu

from rcpe import mydb,settings
import json
import os
from rcpe.fresub import loader


def insert(con,fileName,query,name,reverse):
    
    file = open(fileName,'r')
    records=[]
    for line in file:
        line = line.strip()
        r = json.loads(line)
        id = int(r['id'])
        pair = json.dumps(r[name])
        record = (id,pair)
        if reverse:
            record = (pair,id)
        records.append(record)
        if len(records) >100:
            mydb.executeQueryRecords(con,query,records,False)
            records = []
    if len(records) >0:
        mydb.executeQueryRecords(con,query,records,False)
        records = []


def insertTokenFunc(con,pairs,query):
    records = []
    for pair in pairs:
        reasons = []
        consequences = []
        id = ''
        for sent in pair:
            if id == '':
                id = sent.id.split('_')[0]
            sid = sent.id.split('_')[1]
            id += '_'+sid
            if sent.rc == 'R':
                reasons.append(sent)
            elif sent.rc == 'C':
                consequences.append(sent)
        jsonDict = {}
        jsonDict['id']=id
        jsonDict['r']=[sent.tokens for sent in reasons]
        jsonDict['c']=[sent.tokens for sent in consequences]
        jsonStr = json.dumps(jsonDict)
        record = (id,jsonStr)
        records.append(record)
        if len(records) >100:
            mydb.executeQueryRecords(con,query,records,False)
            records = []
    if len(records) >0:
        mydb.executeQueryRecords(con,query,records,False)
        records = []


def main():

    from optparse import OptionParser
   
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-r","--result",dest ='insertResult',action ='store_true', help="insert json result", default = False)
    parser.add_option("-t","--tokenize",dest ='insertToken',action ='store_true', help="insert tokenized rc pairs", default = False)

    (options,args) = parser.parse_args()
    insertResult = options.insertResult
    insertToken = options.insertToken
    

    CONN_STRING = mydb.get_CONN()
    con = mydb.getCon(CONN_STRING)
    dir_path = os.path.join(settings.PROJECT_DIR,'result/raw/')

    if insertResult:

        # create db
        querys = []
        querys.append('drop table if exists rc;')
        querys.append('create table rc(id int,pairs text, tuples text, coref text);')
        mydb.executeManyQuery(con,querys,False)

        # insert pairs
        query =  'insert into rc(id,pairs) values(%s, %s)'
        insert(con,os.path,join(dir_path,'result.sentence.json.txt'),query,'sen_pairs',False)
        # insert tuples
        query = 'update rc set tuples = %s where id = %s'
        insert(con,os.path.join(dir_path,'result.tuple.json.txt'),query,'pairs',True)
        # insert coref
        query = 'update rc set coref = %s where id = %s'
        insert(con,os.path.join(dir_path,'result.coref.json.txt'),query,'coref',True)
    if insertToken:
        querys = []
        querys.append('drop table if exists tokenizedrc;')
        querys.append('create table tokenizedrc(id char(50),tknPair text);')
        mydb.executeManyQuery(con,querys,False)
        
        data = loader.Loader.load()
        pairs = loader.Loader.sent2pair(data)
        query = 'insert into tokenizedrc(id,tknPair) values(%s,%s);'
        insertTokenFunc(con,pairs,query)
        
        
if __name__ == '__main__':
    main()
