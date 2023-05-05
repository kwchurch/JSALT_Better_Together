#!/bin/sh

cd /work/k.church/semantic_scholar/citations/graphs
sort -T /work/k.church/tmp -m citations.piece.???.gz.graph.node_freq.s | $HOME/final/suffix/uniq1.sh > citations.node_freqs

