#!/bin/sh

f=`echo $1 ${SLURM_ARRAY_TASK_ID} | awk '{printf "%s.%03d\n", $1, $2}'`

sort_bigrams $f > $f.sorted
rm $f
