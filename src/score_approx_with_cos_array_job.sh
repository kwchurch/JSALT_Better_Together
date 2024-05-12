#!/bin/sh

inf=`echo $SLURM_ARRAY_TASK_ID | awk '{printf infile, $1}' infile=$1`
out=$inf.better_together_approx

shift

if [ ! -s $out ]
then

echo hostname: `hostname` $SLURM_ARRAY_JOB_ID $SLURM_ARRAY_TASK_ID > $out
 
awk '$0 !~ /[a-z]/ && NF == 5 && $1 != $2' $inf |
cut -f1,2 | 
uniq1.sh | 
awk 'NF > 1' | 
$JSALTsrc/score_approx_with_cos.py $* >> $out

fi 
