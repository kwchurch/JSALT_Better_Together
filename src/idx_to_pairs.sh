#!/bin/sh

dir=$1
batchsize=$2
offset=$3
tmpdir=$4.$$

mkdir -p $tmpdir

$JSALTsrc/C/x_to_y La  |
awk 'BEGIN {FS=OFS="\t"}; 
      {for(i in ring_buffer) printf "%09d\t%09d\n", ring_buffer[i]+0, $1}
      {ring_buffer[NR % N] = $1}' N=$offset | 
split -l $batchsize - $tmpdir/x.

for f in $tmpdir/x.*
do
sort -u -T . -S '90%' $f |
$JSALTsrc/C/pairs_to_cos --dir $dir --input_new_pairs
done

rm -rf $tmpdir




