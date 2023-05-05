#!/bin/sh

input=$1
outdir=$2
mkdir -p $outdir

src=/work/k.church/semantic_scholar/citations/graphs/src
PATH=$PATH:$src/C

q=" -t 1209 -p short "

pieces=$outdir/x
out=$pieces.split_binary_records

job1=`sbatch -o $out.out -e $out.err $q split_binary_records.sh -pieces 256 -record_size 12 -filename $input -prefix $pieces | awk '{print $NF}'`
job1a=`sbatch $q -d afterok:$job1   --array=0-255 check_bigrams.sh $pieces | awk '{print $NF}'`

job2=`sbatch $q -d afterok:$job1a   --array=0-255 sort_bigrams.sh  $pieces      | awk '{print $NF}'`
job2a=`sbatch $q  -d afterok:$job2  --array=0-255 check_bigrams.sh $pieces sorted | awk '{print $NF}'`

job3=`sbatch $q -d afterok:$job2a   --array=0-127 merge_bigrams.sh $pieces 0 128 | awk '{print $NF}'`
job3a=`sbatch $q -d afterok:$job3   --array=0-127 check_bigrams.sh $pieces merged.0 | awk '{print $NF}'`

job4=`sbatch $q -d afterok:$job3a   --array=0-63  merge_bigrams.sh $pieces 1  64 | awk '{print $NF}'`
job4a=`sbatch $q -d afterok:$job4   --array=0-63 check_bigrams.sh $pieces  merged.1 | awk '{print $NF}'`

job5=`sbatch $q -d afterok:$job4a   --array=0-31  merge_bigrams.sh $pieces 2  32 | awk '{print $NF}'`
job5a=`sbatch $q -d afterok:$job5   --array=0-31 check_bigrams.sh $pieces  merged.2 | awk '{print $NF}'`

job6=`sbatch $q -d afterok:$job5a   --array=0-15  merge_bigrams.sh $pieces 3  16 | awk '{print $NF}'`
job6a=`sbatch $q -d afterok:$job6   --array=0-15 check_bigrams.sh $pieces  merged.3 | awk '{print $NF}'`

job7=`sbatch $q -d afterok:$job6a   --array=0-7   merge_bigrams.sh $pieces 4   8 | awk '{print $NF}'`
job7a=`sbatch $q -d afterok:$job7   --array=0-7 check_bigrams.sh $pieces   merged.4 | awk '{print $NF}'`

job8=`sbatch $q -d afterok:$job7a   --array=0-3   merge_bigrams.sh $pieces 5   4 | awk '{print $NF}'`
job8a=`sbatch $q -d afterok:$job8   --array=0-3 check_bigrams.sh $pieces   merged.5 | awk '{print $NF}'`

job9=`sbatch $q -d afterok:$job8a   --array=0-1   merge_bigrams.sh $pieces 6   2 | awk '{print $NF}'`
job9a=`sbatch $q -d afterok:$job9   --array=0-1 check_bigrams.sh $pieces   merged.6 | awk '{print $NF}'`

job10=`sbatch $q  -d afterok:$job9a --array=0     merge_bigrams.sh $pieces 7   1 | awk '{print $NF}'`
job10a=`sbatch $q -d afterok:$job10 --array=0 check_bigrams.sh $pieces     merged.7 | awk '{print $NF}'`
