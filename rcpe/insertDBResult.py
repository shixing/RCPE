import mydb
import json

def insert(con,fileName,query,name,reverse):
    
    file = open(fileName,'r')
    records=[]
    for line in file:
        line = line.strip()
        r = json.loads(line)
        id = int(r['id'])
        pair = json.dumps(r[name])
        record = (id,pair)
        if reverse:
            record = (pair,id)
        records.append(record)
        if len(records) >100:
            mydb.executeQueryRecords(con,query,records,False)
            records = []
    if len(records) >0:
        mydb.executeQueryRecords(con,query,records,False)
        records = []


def main():
    
    CONN_STRING = mydb.get_CONN('wiki')
    con = mydb.getCon(CONN_STRING)
    
    # create db
    querys = []
    querys.append('drop table if exists rc;')
    querys.append('create table rc(id int,pairs text, tuples text, coref text);')
    mydb.executeManyQuery(con,querys,False)

    # insert pairs
    query =  'insert into rc(id,pairs) values(%s, %s)'
    insert(con,'result.sentence.json.txt',query,'sen_pairs',False)
    # insert tuples
    query = 'update rc set tuples = %s where id = %s'
    insert(con,'result.tuple.json.txt',query,'pairs',True)
    # insert tuples
    query = 'update rc set coref = %s where id = %s'
    insert(con,'result.coref.json.txt',query,'coref',True)

if __name__ == '__main__':
    main()
