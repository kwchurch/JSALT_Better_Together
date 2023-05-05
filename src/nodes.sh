#!/bin/sh

cat $* | 
tr '\t' '\n' |
egrep . |
awk 'killroy[$1]++ < 1'
