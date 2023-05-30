#!/bin/sh


# K=$1
# floats=$2
# B=$3

floats=$1/embedding.f
source $1/record_size.sh

echo `date` starting floats_to_idx.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

echo 

echo K = $K
echo floats = $floats
echo B = $B

echo

tmp=/scratch/k.church/tmp/`hostname`/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID.B$B.i

echo tmp = $tmp

echo

mkdir -p `dirname $tmp`

seed=$SLURM_ARRAY_TASK_ID
out=$floats.simple.seed$seed.K$K.B$B.idx.$SLURM_ARRAY_TASK_ID.i
$JSALTsrc/C/floats_to_random_bytes $K $B $seed < $floats > $tmp

echo `date` finished floats_to_random_bytes 

$JSALTsrc/C/index_random_bytes $tmp $B --simple_case > $out

echo `date` finished index_random_bytes $out

char_hist < $tmp

echo `date` finished char_hist $tmp

rm $tmp

$JSALTsrc/C/invert_permutation $out > $out.inv

echo `date` finished floats_to_idx.sh




