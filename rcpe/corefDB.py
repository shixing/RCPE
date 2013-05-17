#!/usr/bin/python
# -*- coding: utf-8 -*-

# corefDB.py
#
# to implement operations about coref in database
# contains creating table, inserting entries and clearing table
#
# Usage: python getConse.py -u user [-c doCreate, -i doInsert, -d doClear] -d dir
# user specifies the username of DB
# default values of c, i and d is false
# dir is the input dir which contains coref files
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


# to create coref table
def createTables(CONN_STRING):
    con = mydb.getCon(CONN_STRING)
    queries = []
    queries.append('create table coref(id int, replace text, primary key(id))')
    mydb.executeManyQuery(con, queries, False)
    con.close()


# to insert coref sentences
def insertCorefs(dir):
    #files = ['data0.3.txt', 'data1.3.txt', 'data2.3.txt', 'data3.3.txt']
    for f in dir:
        insertCoref(f)


def insertCoref(fileName):
    con = mydb.getCon(CONN_STRING)
    json_date = open(fileName)
    data = json.load(json_date)
    
    i = 0
    records = []
    query = "insert into coref(id, replace) values(%s,%s);"
    for key in data:
        if i % 1000 == 0:
            print i
        i += 1
        
        id = key
        txt = json.dumps(data[key])
        records.append((id,txt))
        if len(records) >= 100:
            try:
                mydb.executeQueryRecords(con, query,records, False)
            except psycopg2.DatabaseError, e:
                print 'Error %s' % e
            records = []
    try:
        if len(records) >0:
            mydb.executeQueryRecords(con, query,records,False)
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    json_date.close()
    con.close()


# to clear coref table
def clearTables(CONN_STRING):
    con = mydb.getCon(CONN_STRING)
    queries = list()
    queries.append('delete from coref')
    mydb.executeManyQuery(con, queries, False)
    con.close()
    

if __name__ == '__main__':
    from optparse import OptionParser
   	
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-u",'--user',dest='username',help='username')
    parser.add_option("-c","--create",dest ='create',action ='store_true', help="create coref", default = False)
    parser.add_option("-i","--insert",dest ='insert',action ='store_true', help="insert coref", default = False)
    parser.add_option("-c","--claer",dest ='clear',action ='store_true', help="delete coref", default = False)
    parser.add_option("-d","--dir",dest ='dir', help="input dir")
    (options,args) = parser.parse_args()
    username = options.username
    create = options.create
    insert = options.insert
    clear = options.clear
    dir = options.dir
    
    CONN_STRING = mydb.get_CONN(username)
    if create:
        createTables(CONN_STRING)
    elif insert:
        insertCorefs(dir)
    elif clear:
        clearTables(CONN_STRING)
        
