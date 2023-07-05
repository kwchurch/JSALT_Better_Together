#!/bin/bash

#Run with sbatch --array 1-10 -N1 jobs/bin_to_bin.slurm

#SBATCH --ntasks=32
#SBATCH --mem=64g
#SBATCH --time=01:00:00
#SBATCH --qos=preemptable
#SBATCH -J bin_to_bin
#SBATCH -o slurm_outputs/S-bintobin-%x-%j.out

module purge
module load python

cd /projects/abeb4417/jsalt/
source jsalt_startup.sh 

cd evaluation/

python sample_bin_local.py --shard_id $SLURM_ARRAY_TASK_ID