import mydb
import json
from pprint import pprint
import psycopg2
import nltk
import os
import re


def createTables(CONN_STRING):
    con = mydb.getCon(CONN_STRING)
    queries = []
    queries.append('create table coref(id int, replace text, primary key(id))')
    mydb.executeManyQuery(con, queries, False)
    con.close()

def insertCorefs():
    files = ['data0.3.txt', 'data1.3.txt', 'data2.3.txt', 'data3.3.txt']
    for f in files:
        insertCoref(f)

def insertCoref(fileName):
    con = mydb.getCon(CONN_STRING)
    json_date = open(fileName)
    data = json.load(json_date)
    #print data
    #return
    i = 0

    records = []
    query = "insert into coref(id, replace) values(%s,%s);"
    for key in data:
        if i % 1000 == 0:
            print i
        #if i > 100:
        #    return
        i += 1
        
        id = key
        txt = json.dumps(data[key])
        records.append((id,txt))
        if len(records) >= 100:
            try:
                mydb.executeQueryRecords(con, query,records, False)
                #print queries
            except psycopg2.DatabaseError, e:
                print 'Error %s' % e
            records = []
        #print data[key]
    try:
        if len(records) >0:
            mydb.executeQueryRecords(con, query,records,False)
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    json_date.close()
    con.close()

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
    parser.add_option("-d","--delete",dest ='delete',action ='store_true', help="delete coref", default = False)
    #parser.add_option("-s","--start", dest='start',help="start id")
    (options,args) = parser.parse_args()
    username = options.username
    create = options.create
    insert = options.insert
    delete = options.delete
    CONN_STRING = mydb.get_CONN(username)
    if create:
        createTables(CONN_STRING)
    elif insert:
        insertCorefs()
    else:
        clearTables(CONN_STRING)
        
