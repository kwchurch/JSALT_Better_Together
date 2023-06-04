#!/bin/sh

N=$1

$JSALTsrc/C/x_to_y La |
awk 'BEGIN {FS=OFS="\t"}; 
      {for(i in ring_buffer) print ring_buffer[i]+0, $1}
      {ring_buffer[NR % N] = $1}' N=$N | 
sort -u -T . -S '90%' 


