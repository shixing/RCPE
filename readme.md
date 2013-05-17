Reason Consequence Pairs Extraction (RCPE)
==========================================

### System Pipeline



### External tools

* Download the SPADE parser at: http://www.isi.edu/~marcu/ -> Software -> Discourse -> Sentence level PArsing of DiscourseE (SPADE). There maybe some bugs in the code, please contact us to get the revised code

* Download Reference Resolver [todo for aihe]

* Get yelp challenge data at http://www.yelp.com/dataset_challenge/ or contact us to get it.

### Preprocess

* Create the user 'wiki'and create 'yelp' database, here we use Postgresql:

```
sudo su root
su - postgres
psql
postgres=# create user wiki with password 'wiki';
postgres=# create database wiki;
postgres=#  GRANT ALL PRIVILEGES ON DATABASE wiki to wiki;
postgres=# \q
```

* Change settings.py to reflect the database setting.

* insert yelp review file into database:
```
python preprocess.py -u -i -f ./yelp/yelp_review.json
```
-f option should be provided the json file path.

* discourse segmenting
```
python preprocess.py -s 0 -e 1000 -f sent.txt -d ../../dp/SPADE/bin
```
-d option should provide the where the SPADE/bin is located. Here, sent.txt would 

Now, the reviews would be splited into clauses and stored in table rc's review_clauses column

### Extract Pairs

* We need to first extract 


### Database Description

* business: Store the business name and relevant information.
* users: Store the user information
* reviews: Store the review text and relavant information. The review_clauses column would store the results of SPADE parser.
* rc: Store the extracted reason-consequence pairs and the reference resolution results.

---

**Contact**

- Xing Shi xingshi@usc.edu
- Ai He aihe@usc.edu
