#!/usr/bin/python
# -*- coding: utf-8 -*-

# getReas.py
#
# to get reasons from file and then write them into a file for each ID
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


def getReas(j):
    iden = str(j['id'])
    rcs = j['sen_pairs']
    reasons = []
    
    # rcs is reasons & consequences pair
    for rc in rcs:
		# to get reasons
        rs = rc[0]
        if len(rs) > 1:
            #print iden
        for r in rs:
            rMap = {}
            #print iden, c
            rMap['id'] = iden + '_' +  str(r[1])
            rMap['txt'] = r[0]
            reasons.append(rMap)
    return reasons


if __name__ == '__main__':
    #dir = 'content_rea/rea/raw/'
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
        reasons = getReas(json.loads(rc))
        for rMap in reasons:
            if not os.path.exists(dir + rMap['id']):
                os.makedirs(dir + rMap['id'])
                f = open(dir + rMap['id'] + '/index.txt', 'w')
                f.write(rMap['txt'].encode('utf-8', errors='ignore'))
                f.close()
    json_data.close()
