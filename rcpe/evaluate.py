import mydb
import json
import rcreplace

def toString(p):
    if p == None:
        return 'None'
    else:
        return str(p)

def tuple2str(phrase):
    s = ''
    s += toString(phrase['subj_adj'])+' '
    s += toString(phrase['subj'])+'|'
    s += toString(phrase['neg'])+' '
    s += toString(phrase['adv'])+' '
    s += toString(phrase['verb'])+'|'
    s += toString(phrase['dobj_adj'])+' '
    s += toString(phrase['dobj'])+'|'
    s += toString(phrase['iobj_adj'])+' '
    s += toString(phrase['iobj'])
    return s

def main():
    offset = 0
    pfile = open('evaluate/evaluate.pairs.'+str(offset)+'.txt','w')
    tfile = open('evaluate/evaluate.tuples.'+str(offset)+'.txt','w')
    cfile = open('evaluate/evaluate.corefs.'+str(offset)+'.txt','w')
    
    CONN_STRING = mydb.get_CONN('wiki')
    con = mydb.getCon(CONN_STRING)
    
    query = 'select * from rc order by id limit 200 offset 0'
    rows = mydb.executeQueryResult(con,query,False)
    
    for row in rows:
        id = int(row[0])
        pairs = json.loads(row[1])
        tuples = json.loads(row[2])
        coref = None
        if row[3]:
            coref = json.loads(row[3])
        
        # write the pairs
        for pair in pairs:
            reasons = pair[0]
            consequences = pair[1]
            for reason in reasons:
                pfile.write(str(id)+'\t'+reason[0]+'\n')
            for consequence in consequences:
                pfile.write(str(id)+'\t'+consequence[0]+'\n')
        
        # write the tuples:
        for t in tuples:
            reasons = t[0]
            consequences = t[1]
            for reason in reasons:
                tfile.write(str(id)+'\t'+tuple2str(reason[0])+'\n')
            for consequence in consequences:
                tfile.write(str(id)+'\t'+tuple2str(consequence[0])+'\n')

        # write the tuples 
        if row[3]:
            corefPairs=rcreplace.mergeCoref(pairs,coref)
            for pair in corefPairs:
                reasons = pair[0]
                consequences = pair[1]
            for reason in reasons:
                cfile.write(str(id)+'\t'+reason+'\n')
            for consequence in consequences:
                cfile.write(str(id)+'\t'+consequence+'\n')

    pfile.close()
    tfile.close()
    cfile.close()

if __name__ == '__main__':
    main()
