#!/usr/bin/python
# -*- coding: utf-8 -*-

# mydb.py
# Provide some common database tasks inferences.
#
# Author: Xing Shi
# contact: xingshi@usc.edu
# 
# see demo() for help

import psycopg2
import sys
import settings


def get_CONN():
    username = settings.Database_User
    password = settings.Database_Password
    dbname = settings.Database_Name
    s =  "host='localhost' dbname='__dbname__' user='__username__' password='__password__'"
    s = s.replace('__dbname__',dbname)
    s = s.replace('__username__',username)
    s = s.replace('__password__',password)
    return s


def getCon(CONN_STRING):
    try:
        con = psycopg2.connect(CONN_STRING)
        con.set_client_encoding('UTF8')
        return con
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(-1)

    
def closeCon(con):
    if con:
        con.close()
     

def executeManyQuery(con,querys,debug):
    try:
        cur = con.cursor()
        for query in querys:
            if debug:
                print query
            cur.execute(query)
            con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(-1)


def executeQuery(con,query,debug):
    try:
        cur = con.cursor()
        if debug:
            print query
        cur.execute(query)
        con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(-1)


def executeQueryRecords(con,query,records,debug):
    try:
        cur = con.cursor()
        if debug:
            print query
        cur.executemany(query,records)
        con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(-1)


def executeQueryResult(con,query,debug):
    try:
        cur = con.cursor()
        if debug:
            print query
        cur.execute(query)
        rows=cur.fetchall()
        return rows
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(-1)


def demo():
    CONN_STRING = get_CONN('wiki')
    con = getCon(CONN_STRING)
    # performe other tasks
    # ...
