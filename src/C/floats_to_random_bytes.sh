#!/bin/sh

K=$1
B=$2
floats=$3

echo date : `date`
echo hostname : `hostname`
echo job : "$SLURM_JOB_ID"_"$SLURM_ARRAY_TASK_ID"
echo seed: "$SLURM_ARRAY_TASK_ID"
echo K : $K
echo B : $B
echo floats : $floats

floats_to_random_bytes $K $B $SLURM_ARRAY_TASK_ID < $floats > $floats.$SLURM_JOB_ID.$SLURM_ARRAY_TASK_ID.B$B.i

