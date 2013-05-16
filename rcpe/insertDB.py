import mydb

file = open('yelp.txt','r')

CONN_STRING = mydb.get_CONN('xingshi')
con = mydb.getCon(CONN_STRING)
query = "update review set review_clauses = %s where id = %s"
records =[]
i = 0
while True:
    line = file.readline()
    if not line:
        mydb.executeQueryRecords(con,query,records,True)
        records=[]
        break
    ll=line.split('\t')
    id = ll[0].strip()
    clause = ll[1].strip()
    record = (clause,id)
    records.append(record)
    if len(records) == 100:
        mydb.executeQueryRecords(con,query,records,True)
        records=[]
    i+=1
    if i % 1000 ==0 :
        print i
    
