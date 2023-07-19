#!/bin/sh

# $1 should be a directory with embedding.f, record_size, etc.

seed=$SLURM_ARRAY_TASK_ID
idx=idx.$seed.i

if [ ! -s $idx ]
then
echo working on $JSALTsrc/C/floats_to_idx.sh $*
$JSALTsrc/C/floats_to_idx.sh $*
fi

# NOTE: there are two files, idx_to_pairs.sh,
# one in $JSALTsrc and the other in $JSALTsrc/C
# We should fix this (it is way too confusing)

if [ ! -s $idx.new_pairs ]
then
echo pwd is: `pwd`
echo working on $JSALTsrc/idx_to_pairs.sh $1 1000000 5 $idx.new_pairs.tmpdir
$JSALTsrc/idx_to_pairs.sh $1 1000000 5 $idx.new_pairs.tmpdir < $idx | awk '$1 > 0.5' > $idx.new_pairs
fi

