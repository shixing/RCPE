#!/bin/python
# -*- coding: utf-8 -*-

# extract_basic.py 
# extract the basic patterns using brute-force
#     1 extract n-gram frequent set
#
# Author: Xing Shi
# contact: xingshi@usc.edu

import settings
from multiprocessing import Process,Queue
from loader import Loader
import os
import operator

def main():

    data = Loader.load()    
    min_n_gram = 2
    max_n_gram = 6
    dir_path = os.path.join(settings.TEMP_DIR,'n_gram/')
    processes = []
    
    #---- frequent n_gram ----
    # for i in xrange(min_n_gram,max_n_gram+1):
    #     p = Process(target = n_gram_group , args = (dir_path,data,i))
    #     processes.append(p)
    #     p.start()
    
    # for p in processes:
    #     p.join()
    
    #---- frequent parse_gram ----
    parse_gram_group(dir_path,data,min_n_gram,max_n_gram)
        
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

if __name__ == "__main__":
    main()
