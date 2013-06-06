#!/bin/python
# -*- coding: utf-8 -*-

# loader.py 
# load the pairs into memory
#
# Author: Xing Shi
# contact: xingshi@usc.edu

from rcpe import settings
import os
import json
from sent import Sent
import cPickle
import threading
import time
from multiprocessing import Process,Queue



class Loader:
    jsonFile = os.path.join(settings.PROJECT_DIR,'result/raw/result.sentence.json.txt')
    pickleFile = os.path.join(settings.TEMP_DIR,'result.sentence.pickle')
    
    
    @staticmethod
    def load(from_scratch=False):
        start = time.time()*1000
        data = None
        if from_scratch:
            data = Loader.load_from_json_multiprocess()
        else:
            if os.path.exists(Loader.pickleFile):
                data= Loader.load_from_pickle()
            else:
                data= Loader.load_from_json()
        end = time.time()*1000
        print end-start,len(data)
        return data

    @staticmethod
    def load_from_json():
        # load from json file and save it as pickle
        data = [] # array of Sent
        jf = open(Loader.jsonFile,'r')
        i=0
        for line in jf:
            if i%100 ==0:
                print i
            i+=1
            jline = json.loads(line)
            id=str(jline['id'])
            sent_pairs = jline['sen_pairs']
            for sent_pair in sent_pairs:
                reasons = sent_pair[0]
                cons = sent_pair[1]
                for reason in reasons:
                    sid = str(reason[1])
                    raw = reason[0]
                    sent = Sent(id+'_'+sid,'R',raw)
                    data.append(sent)
                for consequece in cons:
                    sid = str(consequece[1])
                    raw = consequece[0]
                    sent = Sent(id+'_'+sid,'C',raw)
                    data.append(sent)
         
        # save it into pickle
        cPickle.dump(data,open(Loader.pickleFile,'w'))
        
        return data


    class processJSON(threading.Thread):

        def __init__(self,data,lines,id,num):
            threading.Thread.__init__(self)
            self.data = data
            self.lines = lines
            self.id = id
            self.num = num


        def run(self):
            i=0
            k=0
            for line in self.lines:
                i+=1
                if i % self.num != self.id:
                    continue
                if k%100 ==0:
                    print 't' + str(self.id) + ':' + str(k)
                k+=1
                jline = json.loads(line)
                id=str(jline['id'])
                sent_pairs = jline['sen_pairs']
                for sent_pair in sent_pairs:
                    reasons = sent_pair[0]
                    cons = sent_pair[1]
                    for reason in reasons:
                        sid = str(reason[1])
                        raw = reason[0]
                        sent = Sent(id+'_'+sid,'R',raw)
                        self.data.append(sent)
                    for consequece in cons:
                        sid = str(consequece[1])
                        raw = consequece[0]
                        sent = Sent(id+'_'+sid,'C',raw)
                        self.data.append(sent)


    @staticmethod
    def load_from_json_multithread():
        data = [] # array of Sent
        jf = open(Loader.jsonFile,'r')
        lines = []
        thread_num=2
        for line in jf:
            lines.append(line)
        
        threads=[]
        for i in xrange(thread_num):
            thread = Loader.processJSON(data,lines,i,thread_num)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        

        # save it into pickle
        cPickle.dump(data,open(Loader.pickleFile,'w'))
        
        return data

    
    @staticmethod
    def processJSONs(queue,lines,nid,num):
        from rcpe.stanford_parser import parser
        sp = parser.Parser()
        data = []
        i=0
        k=0
        for line in lines:
            i+=1
            if (i % num) != nid:
                continue
            if k%100 ==0:
                print 't' + str(nid) + ':' + str(k)
            k+=1
            jline = json.loads(line)
            id=str(jline['id'])
            sent_pairs = jline['sen_pairs']
            for sent_pair in sent_pairs:
                reasons = sent_pair[0]
                cons = sent_pair[1]
                for reason in reasons:
                    sid = str(reason[1])
                    raw = reason[0]
                    sent = Sent(id+'_'+sid,'R',raw,sp)
                    data.append(sent)
                for consequece in cons:
                    sid = str(consequece[1])
                    raw = consequece[0]
                    sent = Sent(id+'_'+sid,'C',raw,sp)
                    data.append(sent)
        
        queue.put(data)
  

                    
    @staticmethod
    def load_from_json_multiprocess():
        data = [] # array of Sent
        jf = open(Loader.jsonFile,'r')
        lines = []
        process_num=4
        for line in jf:
            lines.append(line)

        q = Queue()
        processes = []
        for i in xrange(process_num):
            p = Process(target=Loader.processJSONs,args=(q,lines,i,process_num))
            p.start()
            processes.append(p)
        
        for i in xrange(process_num):
            d = q.get()
            print 'len:',len(d)
            data+=d
       
        for p in processes:
            p.join()

        # save it into pickle
        cPickle.dump(data,open(Loader.pickleFile,'w'))

        return data
        
        
    @staticmethod
    def load_from_pickle():
        data = cPickle.load(open(Loader.pickleFile,'r'))
        return data

    
    @staticmethod
    def sent2pair(data):
        idx = -1
        cidx = -1
        new_data = []
        temp = []
        for d in data:
            cidx = d.id.split('_')[0]
            if cidx != idx:
                if len(temp)>0:
                    new_data.append(tuple(temp))
                temp = []
                idx = cidx
            temp.append(d)
        if len(temp)>0:
            new_data.append(tuple(temp))
        
        return new_data


if __name__ == '__main__':
    Loader.load(True)
    
