#!/bin/sh


# K=$1
# floats=$2
# B=$3

seed=$SLURM_ARRAY_TASK_ID
idx=idx.$SLURM_ARRAY_TASK_ID.i

$JSALTsrc/C/floats_to_idx.sh $*
$JSALTsrc/C/idx_to_pairs.sh $idx 1000000 5 $idx.new_pairs
