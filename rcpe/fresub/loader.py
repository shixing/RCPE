#!/bin/python
# -*- coding: utf-8 -*-

# loader.py 
# load the pairs into memory
#
# Author: Xing Shi
# contact: xingshi@usc.edu

import settings
import os
import json
from sent import Sent
import cPickle
import threading
import time

class Loader:
    jsonFile = os.path.join(settings.PROJECT_DIR,'result/raw/result.sentence.json.txt')
    pickleFile = os.path.join(settings.TEMP_DIR,'result.sentence.pickle')
    
    
    @staticmethod
    def load(from_scratch=False):
        start = time.time()*1000
        data = None
        if from_scratch:
            data = Loader.load_from_json_multi()
        else:
            if os.path.exists(Loader.pickleFile):
                data= Loader.load_from_pickle()
            else:
                data= Loader.load_from_json()
        end = time.time()*1000
        print end-start
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
    def load_from_json_multi():
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
    def load_from_pickle():
        data = cPickle.load(open(Loader.pickleFile,'r'))
        return data


if __name__ == '__main__':
    Loader.load(True)
