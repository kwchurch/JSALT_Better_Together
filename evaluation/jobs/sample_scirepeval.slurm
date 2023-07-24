#!/bin/bash

#Run with 'for i in 0 1 2 3 4 5 6 7 8 9; do sbatch --export=ALL,total_splits=9,current_split=${i} jobs/sample_scirepeval.slurm; done' with i ranging from 0 .. 9 inclusive

#SBATCH --ntasks=16
#SBATCH --mem=32g
#SBATCH --time=1-00:00:00
#SBATCH --qos=preemptable
#SBATCH -J samp_scirep_test
#SBATCH -o slurm_outputs/S-%x-%j.out

module purge
module load python

cd /projects/abeb4417/jsalt/
source jsalt_startup.sh 

cd evaluation/

echo ${total_splits}
echo ${current_split}
python sample_scirepeval.py ${total_splits} ${current_split}
