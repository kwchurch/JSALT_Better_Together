#!/bin/sh

cat $* | 
tr '\t' '\n' |
egrep . |
awk '{x[$1]++}; END {for(i in x) print x[i] "\t" i}'
