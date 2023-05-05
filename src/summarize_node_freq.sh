#!/bin/sh

cd /work/k.church/semantic_scholar/citations/graphs
awk '{print $2 "\t" $1}' citations.piece.???.gz.graph.node_freq | 
sort |
$HOME/final/suffix/uniq1.sh > citations.graph.node_freqs
