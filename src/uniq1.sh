#!/bin/sh

awk -F'\t' 'BEGIN {prev="NA"}; $1 == prev {printf "\t%s", $2; next}; 
{printf "\n%s\t%s", $1, $2; prev = $1}; END {print ""}' OFS="\t" $*