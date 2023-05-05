#!/bin/sh

#out=summarize_index/`hostname`/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID
out=`echo $SLURM_ARRAY_TASK_ID | awk '{printf "summarize_index/%04d", $1}'`.`hostname`."$SLURM_ARRAY_JOB_ID"_"$SLURM_ARRAY_TASK_ID"
mkdir -p `dirname $out`

summarize_index $* --piece $SLURM_ARRAY_TASK_ID > $out

