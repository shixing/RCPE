#!/usr/bin/python
# -*- coding: utf-8 -*-

# preprocess.py
# Insert json file into database:
#   review.json.txt: python preprocess.py -i -f ./yelp/yelp_review.json # insert from json
#   
# Do the Discourse Segmenting
#   python preprocess.py -s 0 -e 1000 -f sent.txt -d ../../dp/SPADE/bin
#
# Author: Ai He & Xing Shi
# contact: aihe@usc.edu xingshi@usc.edu

import mydb
import json
from pprint import pprint
import psycopg2
import nltk
import os
import re


#create table users(user_id varchar(50), name varchar(100), review_count int, primary key(user_id));
#create table business(business_id varchar(50), name varchar(100), full_address varchar(100), city varchar(20), state varchar(20), review_count int, categories varchar(20), primary key(business_id));
#create table review(id int, business_id varchar(50), user_id varchar(50), review_text text, review_date date, review_clauses text, primary key(id));

def clearTables(CONN_STRING):
    con = mydb.getCon(CONN_STRING)
    queries = list()
    queries.append('delete from review')
    queries.append('delete from users')
    queries.append('delete from business')
    mydb.executeManyQuery(con, queries, True)

def dropTables(CONN_STRING,text):
    con = mydb.getCon(CONN_STRING)
    queries = list()
    if not text:
        queries.append('drop table if exists review')
        queries.append('drop table if exists users')
        queries.append('drop table if exists business')
        mydb.executeManyQuery(con, queries, True)
    else:
        queries.append('drop table if exists review')
        mydb.executeManyQuery(con, queries, True)


def createTables(CONN_STRING,text):
    con = mydb.getCon(CONN_STRING)
    queries = list()
    if not text:
        queries.append('create table users(user_id varchar(50), name varchar(100), review_count int, primary key(user_id))')
        queries.append('create table business(business_id varchar(50), name varchar(100), full_address varchar(100), city varchar(20), state varchar(20), review_count int, categories varchar(20), primary key(business_id))')
        queries.append('create table review(id int, business_id varchar(50), user_id varchar(50), review_text text, review_date date, review_clauses text, primary key(id))')
        mydb.executeManyQuery(con, queries, True)
    else:
        queries.append('create table review(id int, review_text text, review_clauses text, primary key(id))')
        mydb.executeManyQuery(con, queries, True)

def insertReviews(fileName,text):
    con = mydb.getCon(CONN_STRING)
    json_date = open(fileName,'r')
   # date = json.load(json_date)
    total = 0
    fail = 0
    succ = 0
    for entry in json_date:
        total += 1
        if not text:
            data = json.loads(entry)
            succ += 1
            query = "insert into review(id, business_id, user_id, review_text, review_date) values('"
            query += str(succ) + "', '"
            query += data['business_id'] + "', '"
            query += data['user_id'] + "', '"
            query += data['text'].replace("'","''") +  "', '"
            query += data['date'].replace("'","''") +  "')"
        else:
            succ += 1
            query = "insert into review(id,review_text) values('"
            query += str(succ) + "', '"
            query += entry.replace("'","''") +  "')"

        try:
            mydb.executeQuery(con,query, False)
        except psycopg2.DatabaseError, e:
            fail += 1
            succ -= 1
            print 'Error %s' % e
    
    print succ, fail, total
    json_date.close()
    con.close()

def processSingle(start, end, fileName,dirName,p):
    fileName = os.path.abspath(fileName)
    #totalOneTime = 1000#increment each time
    totalOneTime = end
    con = mydb.getCon(CONN_STRING)
    #nltk.download()
    sent_tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    #text = nltk.corpus.abc.raw('science.txt')
    iter = start
    per = 1
    while iter * per < totalOneTime:
        print iter
        query = "select id, review_text from review order by id LIMIT "+ str(per)+" OFFSET " + str(iter * per)
        resultSet = mydb.executeQueryResult(con, query, False)
        sentLens = list()
        #fileName = 'sents.txt'
        file = open(fileName, 'w')
       
        entry = resultSet[0]
        try:
            sents = sent_tokenizer.tokenize(entry[1])
        except UnicodeDecodeError, e:
            iter += 1
            continue
            
        #sentLens.append([entry[0], len(sents)])
#       fileName = 'sents' + str(iter * 10) + '-' + str(iter* 10 + 10) + '.txt'
        for sent in sents:
            if p.match(sent):
                print sent
                sent = 'Special'
            elif len(sent.split()) > 70:
                print sent
                sent = 'longsentence'
            file.write('<s> ' + sent + ' </s> \n')
        file.close()
        os.system('perl '+dirName+'/spade.pl ' + fileName)
        outputFileName = fileName + '.chp.edu.fmt';

        with open(outputFileName) as f:
            content = f.readlines()
        loc = 0
        #print len(content)
        clauses = list()   
        while loc < len(content):
            subLen = int(content[loc])
            loc += 1
            j = 0

            while j < subLen:
                j += 1   
                if len(content[loc].split()) > 2:
                    clauses.append(content[loc].split(' ', 1)[1].rstrip('\n').replace("'","''"))
                loc += 1
                #print subLen, j, loc
        if len(clauses) < 1:
            iter += 1
            continue
        strClauses = clauses[0]
        for clause in clauses[1:]:
            strClauses += '###' + clause
        query="UPDATE review SET (review_clauses) = ('" + strClauses + "') WHERE id = '"+str(entry[0])+"'"
        
        mydb.executeQuery(con, query, False)
        sentLens = list()
        iter += 1
   
    con.close()

def processBatch(p):
    totalOneTime = 300 #increment each time
    con = mydb.getCon(CONN_STRING)
    #nltk.download()
    sent_tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    #text = nltk.corpus.abc.raw('science.txt')
    iter = 237
    per = 1
    while iter * per < totalOneTime:
        query = "select id, review_text from review order by id LIMIT "+ str(per)+" OFFSET " + str(iter * per)
        resultSet = mydb.executeQueryResult(con, query, False)
        sentLens = list()
        fileName = 'sents.txt'
        file = open(fileName, 'w')

        for entry in resultSet:
            sents = sent_tokenizer.tokenize(entry[1])
            sentLens.append([entry[0], len(sents)])
#            fileName = 'sents' + str(iter * 10) + '-' + str(iter* 10 + 10) + '.txt'
            for sent in sents:
                if p.match(sent):
                    print sent
                    sent = 'Special'
                elif len(sent.split()) > 70:
                    print sent
                    sent = 'longsentence'
                file.write('<s> ' + sent + ' </s> \n')
        file.close()
        print sentLens
        os.system('perl spade.pl ' + fileName)
        outputFileName = 'sents.txt.chp.edu.fmt';
        #outputFile = open(outputFileName, 'r')
        with open(outputFileName) as f:
            content = f.readlines()
        loc = 0
        queries = list()
        print len(content)
        for lens in sentLens:
            i = 0
            clauses = list()
            while i < lens[1]:
                i += 1
                #print lens[0], content[loc]
                subLen = int(content[loc])
                loc += 1
                j = 0
                print subLen
                while j < subLen:
                    print j
                    j += 1   
                    print content[loc],
                    if len(content[loc].split()) > 2:
                        clauses.append(content[loc].split(' ', 1)[1].rstrip('\n').replace("'","''"))
                    loc += 1
                    print subLen, j, loc
                #print clauses
            strClauses = clauses[0]
            for clause in clauses[1:]:
                strClauses += '###' + clause
            query="UPDATE review SET (review_clauses) = ('" + strClauses + "') WHERE id = '"+str(lens[0])+"'"
            #print query
            mydb.executeQuery(con, query, False)
            #queries.append(query)
        #print queries
        #mydb.executeManyQuery(con, queries, False)
        sentLens = list()
        iter += 1
    #sents = sent_tokenizer.tokenize(text)
    #pprint(sents[1:2])
    con.close()

if __name__ == '__main__':
   
    from optparse import OptionParser
   
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i","--insert",dest ='insert',action ='store_true', help="insert reviews", default = False)
    parser.add_option("-s","--start", dest='start',help="start id")
    parser.add_option("-e","--end", dest='end',help="end id")
    parser.add_option("-f","--file", dest='file',help="file name: when insert records, this indicates the source file; when process data, this indicate the temp file path")
    parser.add_option("-d","--dir",dest='dir',help="spade.pl dir")
    parser.add_option("-t","--text",dest='text',action="store_true", default = False , help="input file is txt file ?")
    (options,args) = parser.parse_args()
    insert = options.insert
    text = options.text
    
    CONN_STRING = mydb.get_CONN()
    p = re.compile('^\\W+$')

    print CONN_STRING
    
    
    if insert:
        fileName = options.file
        dropTables(CONN_STRING,text)
        createTables(CONN_STRING,text)
        insertReviews(fileName,text)
    else:
        start = int(options.start)
        end = int(options.end)
        fileName = options.file
        dirName = options.dir
        processSingle(start,end,fileName,dirName,p)
