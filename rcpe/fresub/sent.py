#!/bin/python
# -*- coding: utf-8 -*-

# rcpair.py 
# the class to stroe rc pairs
#
# Author: Xing Shi
# contact: xingshi@usc.edu

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn


class Sent:

    POS_MAP = {'NN':wn.NOUN,'NNS':wn.NOUN,'JJ':wn.ADJ,'VB':wn.VERB,'RB':wn.ADV}
    wnl = WordNetLemmatizer()

    def __init__(self,id,rc,raw):
        self.id = id
        self.rc = rc # 'R' for reason, 'C' for consequece
        self.raw = raw
        self.process()
        
    def process(self):
        if self.raw:
            tokens = nltk.word_tokenize(self.raw)
            temp_pos = nltk.pos_tag(tokens)
            pos = [pos_penn for word,pos_penn in temp_pos]
            stems = []
            for token,pos_penn in temp_pos:
                if pos_penn in Sent.POS_MAP:
                    stem = Sent.wnl.lemmatize(token,Sent.POS_MAP[pos_penn])
                else:
                    stem = token
                stems.append(stem)

            self.tokens = tokens
            self.pos = pos
            self.stems = stems
        
        
if __name__ == '__main__':
    # test
    sentence = 'I like the cars better!'
    sent = Sent('1','R',sentence)
    print sent.raw
    print sent.tokens
    print sent.pos
    print sent.stems
