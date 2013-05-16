import json

def getReas(j):
    iden = str(j['id'])
    rcs = j['sen_pairs']
    reasons = []
    for rc in rcs:
        #print rc
        rs = rc[0]
        #print cs
        if len(rs) > 1:
            print iden
        for r in rs:
            rMap = {}
            #print iden, c
            rMap['id'] = iden + '_' +  str(r[1])
            rMap['txt'] = r[0]
            reasons.append(rMap)
    return reasons

if __name__ == '__main__':
    dir = 'content_rea/rea/raw/'
    import os
    json_data = open('result.sentence.json.txt')
    #f = open('cons.sentence.json.txt', 'w')
    for rc in json_data:
        reasons = getReas(json.loads(rc))
        for rMap in reasons:
            if not os.path.exists(dir + rMap['id']):
                os.makedirs(dir + rMap['id'])
                f = open(dir + rMap['id'] + '/index.txt', 'w')
                f.write(rMap['txt'].encode('utf-8', errors='ignore'))
                f.close()
    json_data.close()
