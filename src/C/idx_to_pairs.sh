#!/bin/sh

infile=`echo $1 $SLURM_ARRAY_TASK_ID | awk '{printf $1, $2}'`
outfile=`echo $2 $SLURM_ARRAY_TASK_ID | awk '{printf $1, $2}'`
offset=$3


echo `date` idx_to_pairs.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

echo 

echo infile = $infile
echo outfile = $outfile
echo offset = $offset

tmp=/scratch/k.church/tmp/`hostname`/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID
echo tmp = $tmp

echo

mkdir -p $tmp

idx_to_pairs --offset $offset --idx $infile |
sort -u -T $tmp --parallel=10 -S "10%" > $outfile

echo `date` idx_to_pairs.sh




