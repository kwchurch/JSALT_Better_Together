#!/bin/sh

f=`echo $1 ${SLURM_ARRAY_TASK_ID} $2 | 
awk 'NF == 1 {print; next}; 
     NF == 2 {printf "%s.%03d\n", $1, $2}
     NF >= 3 {printf "%s.%03d.%s\n", $1, $2, $3}'`

check_bigrams $f > $f.checked

if [ -s $f.sorted ]
then
check_bigrams $f.sorted >> $f.checked
fi

