#!/bin/sh

# K=$1
# B=$2
source $1/record_size.sh
floats=$1/embedding.f

echo date : `date`
echo hostname : `hostname`
echo job : "$SLURM_JOB_ID"_"$SLURM_ARRAY_TASK_ID"
echo seed: "$SLURM_ARRAY_TASK_ID"
echo K : $K
echo B : $B
echo floats : $floats

floats_to_random_bytes $K $B $SLURM_ARRAY_TASK_ID < $floats > $1/idx.$SLURM_ARRAY_TASK_ID.B$B.i

