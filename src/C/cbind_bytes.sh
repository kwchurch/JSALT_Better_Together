#!/bin/sh

N=$1
gap=$2
prefix=$3
suffix=$4

file1=`echo | awk '{print prefix id suffix N ".i"}' N=$N prefix=$prefix suffix=$suffix id=${SLURM_ARRAY_TASK_ID} gap=$gap`
file2=`echo | awk '{print prefix gap+id suffix  N ".i"}' N=$N prefix=$prefix suffix=$suffix id=${SLURM_ARRAY_TASK_ID} gap=$gap`
outfile=`echo | awk '{print prefix id suffix  2*N ".i"}' N=$N prefix=$prefix suffix=$suffix id=${SLURM_ARRAY_TASK_ID} gap=$gap`
cbind_bytes $N $file1 $file2 > $outfile
