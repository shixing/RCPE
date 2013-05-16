import json

def getMap():
    json_data = open('result.sentence.json.txt')
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
    f = open('rcMap.txt', 'w')
    for c in crMap:
        f.write(c + ' ')
        for r in crMap[c]:
            f.write(r + ' ')
        f.write('\n')
    f.close

if __name__ == '__main__':
    getMap()
