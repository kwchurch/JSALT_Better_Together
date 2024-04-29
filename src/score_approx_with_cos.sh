#!/bin/sh

awk '$0 !~ /[a-z]/ && NF == 5 && $1 != $2' |
cut -f1,2 | 
uniq1.sh | 
awk 'NF > 1' | 
$JSALTsrc/score_approx_with_cos.py $*


