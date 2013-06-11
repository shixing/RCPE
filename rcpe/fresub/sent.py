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

class SubString:
    def __init__(self,slist):
        self.slist = tuple(slist)
        self.size = len(slist)
    
    def __hash__(self):
        return hash(self.slist)
    
    def __eq__(self,other):
        return self.slist == other.slist

    def __repr__(self):
        return repr(self.slist)

    def toString(self,stems):
        
        temp=[]
        try:
            for idx in self.slist:
                temp.append(stems[idx])
        except Exception:
            print stems
            print self.slist
        return '_'.join(temp)

class Tree:
    
    def __init__(self,tree,leaves,stems,parent):
        self.depth = tree.depth()
        self.numChildren = tree.numChildren()
        self.isLeaf = tree.isLeaf()
        self.isPreTerminal = tree.isPreTerminal()
        self.isPrePreTerminal = tree.isPrePreTerminal()
        self.isPhrasal = tree.isPhrasal()
        self.value = tree.value()
        self.leafIndex = leaves.indexOf(tree)
        if self.leafIndex != -1:
            try:
                self.stem = stems[self.leafIndex]
            except Exception:
                print stems
                print leaves
                print self.leafIndex
                print self.value
        self.parent = parent
        self.children = []
        self.score = tree.score()
        for child in tree.children():
            ptree = Tree(child,leaves,stems,self)
            self.children.append(ptree)

    def pennString(self,indent=0,childId=0):
        ps = ''
        if self.isPreTerminal == 1:
            ps = '(%s [%.2f] %s [%d])' % (self.value,self.score,self.children[0].value,self.children[0].leafIndex)
            if childId != 0:
                ps = '    '.join(['']*(indent+1)) + ps
        else:
            ps = '    '.join(['']*(indent+1))
            ps += '(%s [%.2f]' % (self.value,self.score)
            if self.children[0].isPreTerminal == 0:
                ps+='\n'
            for i in xrange(len(self.children)):
                child = self.children[i]
                ps+= child.pennString(indent+1,i)
                if i<len(self.children)-1:
                    ps+='\n'
            ps += ')'
        return ps

    # return leaves, substring_set
    def getSubstring(self):
        pos_filter = set(['.'])
        leaves = []
        subset = set()
        if self.isPreTerminal == 1:
            if not self.value in pos_filter:
                leaves.append(self.children[0].leafIndex)
                subset.add(SubString(leaves))
        else:
            for child in self.children:
                cleaves, csubset = child.getSubstring()
                leaves+=cleaves
                subset = subset.union(csubset)
            subset.add(SubString(leaves))
            
        return leaves,subset




class Sent:

    POS_MAP = {'NN':wn.NOUN,'NNS':wn.NOUN,
               'JJ':wn.ADJ,
               'VB':wn.VERB,'VBD':wn.VERB,'VBG':wn.VERB,'VBN':wn.VERB,'VBP':wn.VERB,'VBZ':wn.VERB,
               'RB':wn.ADV}

    wnl = WordNetLemmatizer()

    def __init__(self,id,rc,raw,sp):
        self.id = id
        self.rc = rc # 'R' for reason, 'C' for consequece
        self.raw = raw
        self.sp = sp
        self.process()
        del self.sp
        
    def process(self):
        if self.raw:
            # all token result is based on Stanford Parser
            tokens,tree = self.sp.parse(self.raw)
            tokens = [t.word() for t in tokens]
            temp_pos = nltk.pos_tag(tokens)
            pos = [pos_penn for word,pos_penn in temp_pos]
            stems = []
            for token,pos_penn in temp_pos:
                if pos_penn in Sent.POS_MAP:
                    stem = Sent.wnl.lemmatize(token,Sent.POS_MAP[pos_penn])
                else:
                    stem = token
                stems.append(stem.lower())
            
            self.tokens = tokens
            self.pos = pos
            self.stems = stems
            
            leaves = tree.getLeaves()
            ptree = Tree(tree,leaves,stems,None)
            self.tree = ptree
        
        
        
if __name__ == '__main__':
    # test
    from rcpe.stanford_parser import parser
    sp = parser.Parser()
    sentence = 'I loved you!'
    sent = Sent('1','R',sentence,sp)
    print sent.raw
    print sent.tokens
    print sent.pos
    print sent.stems
    print sent.tree.pennString()
    leaves, substrs = sent.tree.getSubstring()
    print substrs
    for sb in substrs:
        print sb.toString(sent.stems)
