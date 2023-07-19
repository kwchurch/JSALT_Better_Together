#!/bin/sh

tmp=/tmp/pairs_to_cos.$$

cat - > $tmp.input

if [ $# == 0 ]
then

    echo `awk -F/ '{print $NF}' $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt` id1 id2 | tr ' ' '\t'

    for emb in `cat $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt`
    do
    $JSALTsrc/C/pairs_to_cos --dir $JSALTdir/semantic_scholar/embeddings/$emb < $tmp.input 
    done | 
    awk '{printf "%0.3f\n", $1}' |
    $JSALTsrc/reshape.py -1 `wc -l $tmp.input` |
    tr ' ' '\t'  |
    paste - $tmp.input |
    sort -nr

else

    echo `echo $*` id1 id2 | tr ' ' '\t'

    for emb in $*
    do
    $JSALTsrc/C/pairs_to_cos --dir $emb < $tmp.input 
    done | 
    awk '{printf "%0.3f\n", $1}' |
    $JSALTsrc/reshape.py -1 `wc -l $tmp.input` |
    tr ' ' '\t'  |
    paste - $tmp.input |
    sort -nr

fi

rm $tmp.input

