#!/bin/sh

# gensim fails when vectors are too short

w2v=$1
tmp=/scratch/k.church/tmp/filter_w2v/`hostname`/$$/`basename $w2v`
mkdir -p `dirname $tmp`
awk 'NF < 2 {next};
    {x=0; 
     for(i=2;i<=NF;i++) x+= ($i * $i);
     if(x > short) print $0}' short=1e-20 $w2v > $tmp

awk 'END {print NR, NF-1}' $tmp
cat $tmp
rm $tmp
