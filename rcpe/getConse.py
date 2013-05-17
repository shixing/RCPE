#!/usr/bin/python
# -*- coding: utf-8 -*-

# getConse.py
#
# to get consequences from file and then write them into a file for each ID
# these files can be used in clustering
# format of input file:
# {"sen_pairs": [[[["because I 've heard so many good things about this place . ", 36]], [["It 's odd , ", 35]]]], "id": 54235}
#
# usage: python getConse.py -f file -d dir
# file - the path to input file
# dir - where to put these files
#
# Author: Ai He
# contact: aihe@usc.edu

import json


def getCons(j):
    iden = str(j['id'])
    rcs = j['sen_pairs']
    cMap = {}
    
    # rcs is reasons & consequences pair
    for rc in rcs:
    	# to get consequences
        cs = rc[1]
        for c in cs:
            #print iden, c
            cMap['id'] = iden + '_' +  str(c[1])
            cMap['txt'] = c[0]
    return cMap            


if __name__ == '__main__':
    #dir = 'content/final/raw/'
    from optparse import OptionParser
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f","--file",dest='file',help="input file name")
    parser.add_option("-d","--dir",dest='dir',help="objectice directory")
    (options,args) = parser.parse_args()
    dir = options.dir
    file = options.file
    
    import os
    #json_data = open('result.sentence.json.txt')
    json_data = open(file)
    for rc in json_data:
        cMap = getCons(json.loads(rc))
        if not os.path.exists(dir + cMap['id']):
            os.makedirs(dir + cMap['id'])
        f = open(dir + cMap['id'] + '/index.txt', 'w')
        f.write(cMap['txt'].encode('utf-8', errors='ignore'))
        f.close()
    json_data.close()
