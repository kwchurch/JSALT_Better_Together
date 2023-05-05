#!/bin/sh


echo $1 |
/work/k.church/semantic_scholar/citations/graphs/src/C/BFS /work/k.church/semantic_scholar/citations/graphs/citations.G -max_depth 5 -print_steps -no_destination |
cut -f2- |
awk '$1 <= 5 {print rand() "\t" $0}' | 
sort | 
awk 'killroy[$2]++ < 6' | 
cut -f2-
