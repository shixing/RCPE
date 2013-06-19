#!/bin/bash

#remove the repeated lines;
sort $1 | uniq -c | sort -k1,1nr | awk '$1<2 && NF>30 {$1=""; print $0;}' > $1.unic

# remove those non-printable lines:
sed -E 's/([^a-zA-Z0-9[:punct:][:space:]]|[€¢®§])//g' $1.unic > $1.print

# remove some system generated lines:

sed -E -e 's/\[(Group|User|Tag|Network):.*\]//g' -e '/https?:\/\//d' -e '/[tT]ake a moment to welcome/d' \
-e 's/&[a-z]{1,8};//g' $1.print >$1.clean  

