#!/bin/bash

#sbatch --array 1-30 -N1 sample.slurm

#SBATCH --ntasks=32
#SBATCH --mem=64g
#SBATCH --time=01:00:00
#SBATCH --qos=preemptable
#SBATCH -J sample
#SBATCH -o slurm_outputs/S-%x-%j.out

cd /projects/abeb4417/
source jsalt_startup.sh 

cd lm_perplexity

./sample.sh $SLURM_ARRAY_TASK_ID
