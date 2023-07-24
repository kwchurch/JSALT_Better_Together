#!/bin/bash

#sbatch --array 1-30 -N1 sample_to_bin.slurm

#SBATCH --ntasks=32
#SBATCH --mem=64g
#SBATCH --time=01:00:00
#SBATCH --qos=preemptable
#SBATCH -J sample_to_bin
#SBATCH -o slurm_outputs/S-%x-%j.out

cd /projects/abeb4417/
source jsalt_startup.sh 

cd lm_perplexity

./sample_to_bin.sh $SLURM_ARRAY_TASK_ID
