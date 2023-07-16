#!/bin/sh

K=$1
seed=$2

tmp=/tmp/Annika.$$

# cat /tmp/Annika/Annika.proposed.vec | 
python $JSALTsrc/Annika/vec_to_kmeans.py --output_centroids --verbose --seed $seed -K $K > $tmp

for i in `seq 1 $K`
do
echo 
echo cluster $i
awk 'NR == i' i=$i $tmp |
tr ' ' '\n' |
$JSALTsrc/C/x_to_y af |
$JSALTsrc/C/vector_near_with_floats --dir $proposed --offset 5 $proposed/idx.*.i | sort -u | sort -nr | head | cut -f2 | 
$JSALTsrc/fetch_from_semantic_scholar_api.py --fields title | 
python $JSALTsrc/Annika/json2txt.py paperId title
done

rm $tmp
