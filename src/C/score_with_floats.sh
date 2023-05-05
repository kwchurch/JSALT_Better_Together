#!/bin/sh

K=$1
floats=$2
nchoices=$3
shift;shift;shift

tmp=/tmp/random_choice.$$

N=`ls -lL $floats | awk '{print $5/(K*4) - 1}' K=$K`

# echo N = $N

random_choice.py $N $nchoices $tmp
x_to_y La < $tmp | score_with_floats --record_size $K --floats $floats --summarize $* 
# |
# awk '{print; for(i=1;i<NF;i++) sums[i] += $i};
#      END {for(i=1;i<NF;i++) printf("%f\t", sums[i]/NR); print "totals"}'

rm $tmp

