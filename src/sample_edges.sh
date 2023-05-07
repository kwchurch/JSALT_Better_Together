#!/bin/sh

S=0.1
K=50
outdir=/scratch/k.church/semantic_scholar/releases/2022-08-23/database/citations/graphs/S$S/K$K/$SLURM_ARRAY_TASK_ID
mkdir -p $outdir

