#!/bin/sh

outdir=$1
query=$2
nbest=$3
mkdir -p $outdir/near2 $outdir/near2.md

echo $query | $JSALTsrc/fetch_references_and_citations.py |
awk '/ERROR/ {next}; $1 == "reference" {print $2; print $3}' | 
awk 'killroy[$1]++ < 1' > $outdir/ids.txt

cat $outdir/ids.txt |
while read p
do
$JSALTsrc/near2.sh $p $nbest > $outdir/near2/$p

cut -f3- $outdir/near2/$p | 
$JSALTsrc/fetch_snippet.py |
paste $outdir/near2/$p - | 
awk 'BEGIN {FS=OFS="\t"; print "embedding", "cos", "id1", "id2", "paper1", "paper2"}; {print}' | 
$JSALTsrc/tsv_to_html.sh > $outdir/near2.md/$p.md

done

echo `cat $JSALTdir/semantic_scholar/embeddings/all_embeddings.txt` > $outdir/scores.txt

cat $outdir/near2/* | cut -f3- | awk '$1 != $2' | sort -u |
$JSALTsrc/pairs_to_cos.sh >> $outdir/scores.txt

$JSALTsrc/tsv_to_html.sh < $outdir/scores.txt > $outdir/scores.md


