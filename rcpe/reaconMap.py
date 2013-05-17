#!/usr/bin/python
# -*- coding: utf-8 -*-

# reaconMap.py
#
# to get consequence-reasons map
# basically, there might be several reasons for a consequence
# format of input file:
# {"sen_pairs": [[[["because I 've heard so many good things about this place . ", 36]], [["It 's odd , ", 35]]]], "id": 54235}
# format of output file:
# consequence_clause_id  reason_clause_id1 reason_clause_id2 ...
#
# Usage: python reaconMap.py -i input -o output
# input - path to input file
# output - path to output file
#
# Author: Ai He
# contact: aihe@usc.edu


import json


def getMap(input, output):
    json_data = open(input)
    crMap = {}
    for entry in json_data:
        data = json.loads(entry)
        iden = str(data['id'])
        rcs = data['sen_pairs']
        for rc in rcs:
            rs = rc[0]
            cs = rc[1]
            crMap[iden + '_' + str(cs[0][1])] = []
            for r in rs:
                crMap[iden + '_' + str(cs[0][1])].append(iden + '_' + str(r[1]))
    #print crMap
    f = open(output, 'w')
    for c in crMap:
        f.write(c + ' ')
        for r in crMap[c]:
            f.write(r + ' ')
        f.write('\n')
    f.close


if __name__ == '__main__':
	from optparse import OptionParser
   	
    # option
    usage="usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i","--input",dest ='input', help="path to input file")
    parser.add_option("-o","--output",dest ='output', help="path to out file")
    (options,args) = parser.parse_args()
    input = options.input
    output = options.output
    
    getMap(input, output)
