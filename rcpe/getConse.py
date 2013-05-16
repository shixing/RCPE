import json

def getCons(j):
    iden = str(j['id'])
    rcs = j['sen_pairs']
    cMap = {}
    for rc in rcs:
        #print rc
        cs = rc[1]
        #print cs
        for c in cs:
            #print iden, c
            cMap['id'] = iden + '_' +  str(c[1])
            cMap['txt'] = c[0]
    return cMap            

if __name__ == '__main__':
    dir = 'content/final/raw/'
    import os
    json_data = open('result.sentence.json.txt')
    #f = open('cons.sentence.json.txt', 'w')
    for rc in json_data:
        cMap = getCons(json.loads(rc))
        if not os.path.exists(dir + cMap['id']):
            os.makedirs(dir + cMap['id'])
        f = open(dir + cMap['id'] + '/index.txt', 'w')
        f.write(cMap['txt'].encode('utf-8', errors='ignore'))
        f.close()
    json_data.close()
