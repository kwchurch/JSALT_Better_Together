#!/bin/bash


#SBATCH --ntasks=32
#SBATCH --mem=32g
#SBATCH --time=2-00:00:00
#SBATCh --partition=blanca-kann
#SBATCH --qos=blanca-kann
#SBATCh --gres=gpu:1
#SBATCH -J every_5_scibert
#SBATCH -o slurm_outputs/S-%x-%j.out

cd /projects/abeb4417/
source jsalt_startup.sh 

./scripts/score_all.sh allenai/scibert_scivocab_cased
