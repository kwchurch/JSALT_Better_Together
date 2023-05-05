#!/bin/sh

K=$1
floats=$2
idx=`echo $3 $SLURM_ARRAY_TASK_ID | awk '{printf $1, $2}'`

echo `date` starting idx_to_cos.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

echo 

echo K = $K
echo floats = $floats
echo idx = $idx

print_floats_index $floats $idx $K --binary > $idx.floats

echo `date` finishing idx_to_cos.sh
