#!/bin/sh

# $1 is a prefix
# $2 is a layer
# $3 is an offset

echo | 
awk '{ out1 = sprintf("%s.%03d.merged.%d",  prefix, id, layer)
      if(layer == 0) {
         in1 = sprintf("%s.%03d.sorted", prefix, id)
         in2 = sprintf("%s.%03d.sorted", prefix, offset + id)
       }
      else  {
         in1 = sprintf("%s.%03d.merged.%d", prefix, id, layer-1)
         in2 = sprintf("%s.%03d.merged.%d", prefix, offset + id , layer-1)
       }
     print "sort_bigrams -m " in1, in2 " | uniq_bigrams > " out1
     print "rm ", in1, in2
}' prefix="$1" layer="$2" offset="$3" id="${SLURM_ARRAY_TASK_ID}" | sh 






