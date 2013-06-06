#!/bin/python
# -*- coding: utf-8 -*-

# extract_basic.py 
# extract the basic patterns using brute-force
#     1 extract n-gram frequent set
#
# Author: Xing Shi
# contact: xingshi@usc.edu

from rcpe import settings
from multiprocessing import Process,Queue
from loader import Loader
import os
import operator
from collections import defaultdict
from functools import partial
import cPickle
import math

def main():

    data = Loader.load()    
    min_n_gram = 2
    max_n_gram = 6
    dir_path = os.path.join(settings.TEMP_DIR,'n_gram/')
    
    
    #---- frequent#  n_gram ----
    # processes = []
    # for i in xrange(min_n_gram,max_n_gram+1):
    #     p = Process(target = n_gram_group , args = (dir_path,data,i))
    #     processes.append(p)
    #     p.start()
    
    # for p in processes:
    #     p.join()
    

    #---- frequent parse_gram ----
    # parse_gram_group(dir_path,data,min_n_gram,max_n_gram) 
        
    #---- frequent parse_gram ----
    matrix_group(dir_path,data,min_n_gram,max_n_gram)


#------------------------------ extract frequent n-gram from stem words--------------
def n_gram_group(dir_path,data,n_gram):
    result_map = {}
    processes = []
    n_process = 4
    q = Queue()
    for i in xrange(n_process):
        p = Process(target=n_gram_worker, args = (data,n_gram,i,n_process,q))
        processes.append(p)
        p.start()
    
    for i in xrange(n_process):
        d = q.get()
        for key in d:
            if key in result_map:
                result_map[key]+=d[key]
            else:
                result_map[key] = d[key]

    for p in processes:
        p.join()
    
    result_map = sorted(result_map.iteritems(), key=operator.itemgetter(1),reverse=True)
    
    f = open(os.path.join(dir_path,'r_%d.txt' % (n_gram,)),'w')
    for key,rank in result_map:
        f.write('%s %d\n' % (key.encode('utf8'),rank))
    
    f.close()

def n_gram_worker(data,n_gram,r,b,queue):
    n_gram_map = {}
    for i in xrange(len(data)):
        if i%b ==r:
            sent = data[i]
            stems = sent.stems
            for i in xrange(len(stems)-n_gram+1):
                s = '_'.join(stems[i:i+n_gram])
                if s not in n_gram_map:
                    n_gram_map[s] = 1
                else:
                    n_gram_map[s] += 1
    queue.put(n_gram_map)

#------------------------------/ extract frequent n-gram from stem words--------------


#------------------------------ extract frequent parse_gram from stem words--------------

def parse_gram_group(dir_path,data,min_n_gram,max_n_gram):
    result_map = {}
    processes = []
    n_process = 4
    q = Queue()
    for i in xrange(n_process):
        p = Process(target=parse_gram_worker, args = (data,i,n_process,q,min_n_gram,max_n_gram))
        processes.append(p)
        p.start()
    
    for i in xrange(n_process):
        d = q.get()
        for key in d:
            if key in result_map:
                result_map[key]+=d[key]
            else:
                result_map[key] = d[key]

    for p in processes:
        p.join()
    
    result_map = sorted(result_map.iteritems(), key=operator.itemgetter(1),reverse=True)
    
    f = open(os.path.join(dir_path,'parse_gram.txt'),'w')
    for key,rank in result_map:
        f.write('%s %d\n' % (key.encode('utf8'),rank))
    
    f.close()

def parse_gram_worker(data,r,b,queue,min_n_gram,max_n_gram):
    parse_gram_map = {}
    for i in xrange(len(data)):
        if i%b ==r:
            sent = data[i]
            leaves,substring = sent.tree.getSubstring() 
            stems = sent.stems
            for sb in substring:
                if sb.size<=max_n_gram and sb.size>=min_n_gram:
                    sbstr = sb.toString(stems)
                    if sbstr in parse_gram_map:
                        parse_gram_map[sbstr]+=1
                    else:
                        parse_gram_map[sbstr] = 1
    queue.put(parse_gram_map)

#------------------------------/ extract frequent parse_gram from stem words--------------

#------------------------------calculate matrix --------------
def calculate_npmi(dir_path,matrix,rdict,cdict,n):
    '''
    npmi(x,y) = pmi(x,y) / -log(p(x,y))
    pmi(x,y) = log( p(x,y) / ( p(x)*p(y) )
    npmi(x,y) = ( log(n(x)*n(y)) - 2 logN ) / ( log( n(x,y) ) - log N) - 1
    '''
    pmi = defaultdict(partial(defaultdict,float))
    pmi_tuple = []

    for rs in matrix:
        for cs in matrix[rs]:
            npmi_top = math.log( rdict[rs] * cdict[cs] ) - 2*math.log(n)
            npmi_bot = math.log( matrix[rs][cs] ) - math.log(n)
            npmi = npmi_top / npmi_bot - 1.0
            #print matrix[rs][cs],rdict[rs],cdict[cs],npmi_top,npmi_bot
            pmi[rs][cs] = npmi
            pmi_tuple.append( (rs,cs,npmi) )
            
    pmi_tuple=sorted(pmi_tuple, key=operator.itemgetter(2),reverse=True)
    
    f = open(os.path.join(dir_path,'pmi.pickle'),'w')
    cPickle.dump(pmi,f)
    f.close()
    
    f = open(os.path.join(dir_path,'pmi.txt'),'w')
    for rs,cs,npmi in pmi_tuple:
        f.write('\t'.join([rs,cs,str(npmi),str(matrix[rs][cs])])+'\n')
    f.close() 


def matrix_group(dir_path,data,min_n_gram,max_n_gram):
    data_tuple = Loader.sent2pair(data)
    result_matrix = defaultdict(partial(defaultdict,int))
    rdict = defaultdict(int)
    cdict = defaultdict(int)
    processes = []
    n_process = 4
    q = Queue()
    for i in xrange(n_process):
        p = Process(target=matrix_worker, args = (data_tuple,i,n_process,q,min_n_gram,max_n_gram))
        processes.append(p)
        p.start()
    
    for i in xrange(n_process):
        (d,rd,cd) = q.get()
        for k1 in d:
            for k2 in d[k1]:
                result_matrix[k1][k2] += d[k1][k2]
        for rk in rd:
            rdict[rk]+=1
        for ck in cd:
            cdict[ck]+=1

    for p in processes:
        p.join()
    
    print 'writing data into pickle ...'
    
    f = open(os.path.join(dir_path,'parse_matrix.pickle'),'w')
    cPickle.dump(result_matrix,f)
    f.close()
    
    f = open(os.path.join(dir_path,'parse_rdict.pickle'),'w')
    cPickle.dump(rdict,f)
    f.close()
    
    f = open(os.path.join(dir_path,'parse_cdict.pickle'),'w')
    cPickle.dump(cdict,f)
    f.close()
    
    print 'calculating npmi ...'
    
    calculate_npmi(dir_path,result_matrix,rdict,cdict,len(data_tuple))


def matrix_worker(data_tuple,r,b,queue,min_n_gram,max_n_gram):
    matrix = defaultdict(partial(defaultdict,int))
    rdict = defaultdict(int)
    cdict = defaultdict(int)

    for i in xrange(len(data_tuple)):
        if i%b ==r:
            pair = data_tuple[i]
            rsubs = set()
            csubs = set()
            for sent in pair:
                leaves,subs = sent.tree.getSubstring()
                stems = sent.stems
                substrs = [s.toString(stems) for s in subs if s.size<=max_n_gram and s.size>=min_n_gram]
                if sent.rc == 'R':
                    rsubs.update(substrs)
                elif sent.rc == 'C':
                    csubs.update(substrs)
            for rsub in rsubs:
                rdict[rsub]+=1
                for csub in csubs:
                    cdict[csub]+=1
                    matrix[rsub][csub]+=1
            
    queue.put((matrix,rdict,cdict))



#------------------------------/ calculate matrix --------------


if __name__ == "__main__":
    main()
