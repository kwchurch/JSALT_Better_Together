#!/bin/sh

bigrams=$1/bigrams
slurm=`echo $SLURM_ARRAY_TASK_ID | awk '{printf "%03d\n", $1}'`
out=$2.$slurm
tmp=author_to_author_job.`hostname`.$$.$slurm

authors=$JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/authors

$JSALTsrc/C/substream_records --input $bigrams --piece $SLURM_ARRAY_TASK_ID --npieces 1000 --record_size 12 | 
$JSALTsrc/C/authors_to_authors --papers_to_authors $authors/papers_to_authors --max_authors 5 > $tmp

$JSALTsrc/C/sort_lbigrams $tmp | $JSALTsrc/C/uniq_lbigrams --sum < $tmp > $out

rm $tmp
