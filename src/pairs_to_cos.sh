#!/bin/sh

tmp=/tmp/pairs_to_cos.$$

cat - > $tmp.input

# echo $* | tr ' ' '\t'
echo `awk -F/ '{print $NF}' $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt` | tr ' ' '\t'

for emb in `cat $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt`
do
$JSALTsrc/C/pairs_to_cos --dir $JSALTdir/semantic_scholar/embeddings/$emb < $tmp.input 
done | 
awk '{printf "%0.3f\n", $1}' |
$JSALTsrc/reshape.py -1 `wc -l $tmp.input` |
tr ' ' '\t'  |
paste - $tmp.input |
sort -nr

rm $tmp.input

