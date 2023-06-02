#!/bin/sh

query=$1
nbest=$2

# JSALTdir=/work/k.church/JSALT-2023/
# JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

# specter=$JSALTdir/semantic_scholar/embeddings/specter
# proposed=$JSALTdir/semantic_scholar/embeddings/proposed

tmp=/tmp/near2.$$


for emb in `cat $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt`
do
# Find 10 papers near query (using specter embedding)
echo $query | 
$JSALTsrc/near_embedding.sh $JSALTdir/semantic_scholar/embeddings/$emb |
sed "$nbest"q | 
awk '{print emb "\t" $0}' emb=$emb
done

rm -rf "$tmp"*

# |
# $JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/papers/corpusId_to_href --fields '---L' 


