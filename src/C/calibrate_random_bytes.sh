#!/bin/sh

echo hostname = `hostname` 1>&2
echo SLURM_JOB_ID = $SLURM_JOB_ID 1>&2
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID 1>&2

calibrate_random_bytes $*
