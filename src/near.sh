#!/bin/sh

query=$1
nbest=$2

# JSALTdir=/work/k.church/JSALT-2023/
# JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src
echo $JSALTsrc
echo $JSALTdir
specter=$JSALTdir/semantic_scholar/embeddings/specter
proposed=$JSALTdir/semantic_scholar/embeddings/proposed

spectertmp=/tmp/$$.near.specter
proposedtmp=/tmp/$$.near.proposed
bothtmp=/tmp/$$.near.both

# Find 10 papers near query (using specter embedding)
echo $query | $JSALTsrc/near_embedding.sh $specter | sed "$nbest"q > $spectertmp

# Same as above, but replace specter embedding with proposed embedding
echo $query | $JSALTsrc/near_embedding.sh $proposed | sed "$nbest"q > $proposedtmp

cat $spectertmp $proposedtmp | cut -f2- | $JSALTsrc/C/pairs_to_cos --dir $specter > $bothtmp.1
cat $spectertmp $proposedtmp | cut -f2- | $JSALTsrc/C/pairs_to_cos --dir $proposed > $bothtmp.2

paste $bothtmp.[12] | cut -f1,4,6 | awk -F'\t' '{printf "%0.3f\t%0.3f\t%s\n", $1,$2,$3}' | 
$JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/href/corpusId_to_href --fields '--L' |
awk 'BEGIN {OFS="\t"; method="Specter"; print "Method", "cosS", "cosP", "paper"}; 
           {print method, $0}
      NR >= nbest {method="Proposed"}' nbest="$nbest"

rm $spectertmp $proposedtmp $bothtmp.[12]

