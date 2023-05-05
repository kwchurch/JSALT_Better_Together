#!/bin/sh

awk '{print $2 "\t" $1}' $* |
sort -T /work/k.church/tmp 

