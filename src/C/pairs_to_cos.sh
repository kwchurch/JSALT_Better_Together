#!/bin/sh

K=$1;
floats=$2
outfile=`echo $3 $SLURM_ARRAY_TASK_ID | awk '{printf $1, $2}'`
shift;shift;shift

echo `date` starting pairs_to_cos.sh

echo hostname = `hostname`
echo SLURM_JOB_ID = $SLURM_JOB_ID
echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID

echo 

pattern=`echo $SLURM_ARRAY_TASK_ID | awk '{printf "%03d"}'`


echo K = $K
echo floats = $floats
echo outfile = $outfile
echo pattern = $pattern

tmp=/scratch/k.church/tmp/pairs_to_cos/`hostname`/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID
echo tmp = $tmp

mkdir -p $tmp/inputs

for f in $*
do
awk 'substr($1, length($1)-2) == pattern' pattern="$pattern" $f > $tmp/inputs/`basename $f`
done

sort -u -m -T $tmp -S "90%" --parallel=10 $tmp/inputs/* |
pairs_to_cos --floats $floats --record_size $K > $outfile

rm -rf $tmp

echo `date` finishing pairs_to_cos.sh
