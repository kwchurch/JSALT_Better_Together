#!/bin/bash

####################################
#     ARIS slurm script template   #
#                                  #
# Submit script: sbatch filename   #
#                                  #
####################################

#SBATCH --job-name=inference # Job name
#SBATCH --output=inference.%j.out # Stdout (%j expands to jobId)
#SBATCH --error=inference.%j.err # Stderr (%j expands to jobId)
#SBATCH --nodes=1     # Number of nodes requested
#SBATCH --cpus-per-task=1     # Threads per task
#SBATCH --time=12:00:00   # walltime
#SBATCH --mem=300G   # memory per NODE
#SBATCH --partition=gypsum-rtx8000    # Partition
#SBATCH --gres=gpu:1
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=spolisetty@umass.edu


if [ x$SLURM_CPUS_PER_TASK == x ]; then
  export OMP_NUM_THREADS=1
else
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
fi

##### Experiment settings #####
# <<< conda initialize <<

## LOAD MODULES ##
module purge        # clean up loaded modules 


eval "$(conda shell.bash hook)"

conda activate /work/pi_huiguan_umass_edu/sandeep/jsalt-env

# load necessary modules
# module load cuda/11.7.0

## RUN YOUR PROGRAM ##
export BIN_NUMBER=90
export EMBEDDING=scincl
#python3 full_specter.py --training-mode valid --bin ${BIN_NUMBER}  --model gat   --embedding ${EMBEDDING} --masked --model-bin 70
#python3 full_specter.py --training-mode valid  --bin ${BIN_NUMBER}  --model sage  --embedding ${EMBEDDING} --masked --model-bin 70
#python3 full_specter.py --training-mode valid --bin ${BIN_NUMBER}  --model gat   --embedding ${EMBEDDING} --masked --no-empty --model-bin 70
python3 full_specter.py --training-mode test --bin ${BIN_NUMBER}  --model gat  --embedding ${EMBEDDING}   --model-bin 70 --normalize

#python3 full_specter.py --training-mode train --bin ${BIN_NUMBER}  --model gat  --normalize --embedding specter --masked
#python3 full_specter.py --training-mode train --bin ${BIN_NUMBER}  --model sage  --normalize --embedding specter --masked
#python3 full_specter.py --training-mode train --bin ${BIN_NUMBER}  --model gat  --normalize --embedding specter --masked --no-empty
#python3 full_specter.py --training-mode train --bin ${BIN_NUMBER}  --model sage  --normalize --embedding specter --masked --no-empty


#python3 full_specter.py --training-mode train --bin ${BIN_NUMBER}  --model sage 
# python3 full_specter.py --training-mode train --bin 70 --model sage --masked
#python3 full_specter.py --training-mode valid --bin 70  --model sage --masked --model-bin ${BIN_NUMBER}


echo "Done"
