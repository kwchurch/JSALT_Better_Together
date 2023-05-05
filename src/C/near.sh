#!/bin/sh

echo `date` near.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

echo $*

echo "---START---"

near $*
