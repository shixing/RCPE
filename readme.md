### insert review file
```
python preprocess.py -u xingshi -i -f ./yelp/yelp_review.json
```
### discourse segmenting
```
python preprocess.py -u xingshi -s 0 -e 1000 -f sent.txt -d ../../dp/SPADE/bin
```