Back-End of RCPE
====================

### Tasks for Back-End
* Build index for business data and reason-consequence pairs
* Respond the request for query business and rc pairs


### Data Description
* Business index: yelp's original business data
* RC pairs index: generated reason-consequence pairs 

### Configuration File
config.xml shouls be placed at the same directory with the runable jar

It has the format as follows:

```
<?xml version="1.0" encoding="UTF-8"?>
<root>
<para bizFile = "yelp_academic_dataset_business.json"/>
<para rcFile = "result.sentence.json.txt"/>
<para bizIdxPath = "bizidx"/>
<para rcIdxPath = "rcidx"/>
<para port = "12345"/>
<para returnNum = "100"/>
</root>
```
* bizFile - path to business data file
* rcFile - path to rc pairs data file
* bizIdxPath - dir to build business index
* rcIdxPath - dir to build rc index
* port - port number to receive request
* returnNum - max number of results to return for a query

### External Tools or Lib
* Lucene
* Dom4j-1.6
* json-lib-2.4
