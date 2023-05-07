#!/bin/sh

query=$1
nbest=$2

JSALTdir=/work/k.church/JSALT-2023/
JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

specter=$JSALTdir/semantic_scholar/embeddings/specter
proposed=$JSALTdir/semantic_scholar/embeddings/proposed

spectertmp=/tmp/$$.near.specter
proposedtmp=/tmp/$$.near.proposed
bothtmp=/tmp/$$.near.both

# Find 10 papers near query (using specter embedding)
echo $query | $JSALTsrc/C/near_with_floats --floats $specter/embedding.K768.f --record_size 768 --offset 5 --map $specter/map $specter/idx.???.i |
cut -f1-3  | sort -nr -u | sed "$nbest"q > $spectertmp

# Same as above, but replace specter embedding with proposed embedding
echo $query | $JSALTsrc/C/near_with_floats --floats $proposed/embedding.K280.f --record_size 280 --offset 5 --map $proposed/map $proposed/idx.??.i |
cut -f1-3  | sort -nr -u | sed "$nbest"q > $proposedtmp

# echo 'Specter'
cat $spectertmp $proposedtmp | cut -f2- | $JSALTsrc/C/pairs_to_cos  --floats $specter/embedding.K768.f --record_size 768 --map $specter/map > $bothtmp.1

cat $spectertmp $proposedtmp | cut -f2- | $JSALTsrc/C/pairs_to_cos  --floats $proposed/embedding.K280.f --record_size 280 --map $proposed/map > $bothtmp.2

paste $bothtmp.[12] | cut -f1,4,6 | awk -F'\t' '{printf "%0.3f\t%s\t%s\n", $1,$2,$3}' | 
$JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/papers/corpusId_to_href --fields '--L' |
awk 'BEGIN {OFS="\t"; method="Specter"; print "Method", "cosS", "cosP", "paper"}; 
           {print method, $0}
      NR >= nbest {method="Proposed"}' nbest="$nbest"

rm $spectertmp $proposedtmp $bothtmp.[12]

