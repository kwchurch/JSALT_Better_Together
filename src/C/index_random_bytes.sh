#!/bin/sh

echo `date` starting index_random_bytes.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

tmp=/tmp/random_permutation.$$.${SLURM_ARRAY_TASK_ID}.i

infile=$1
idx=$infile.idx.${SLURM_ARRAY_TASK_ID}
N=$2
K=$3

if [ ! -s $idx ]
then
echo `date` working on $idx
random_permutation.py $N $tmp
index_random_bytes $infile $tmp > $idx
rm $tmp
fi

# if [ ! -s $idx.hamming_dist16 ]
# then 
# echo `date` working on $idx.hamming_dist16
# print_random_bytes_index $infile $idx $N --binary > $idx.hamming_dist16
# fi

# if [ ! -s $idx.cos ]
# then 
# echo `date` working on $idx.hamming_dist16
# print_floats_index $infile $idx $K --binary > $idx.floats
# fi


if [ ! -s $idx.inv ]
then 
echo `date` working on $idx.inv
invert_permutation $idx > $idx.inv
fi

echo `date` finished index_random_bytes.sh
