#!/bin/sh

offset=$1
shift
N=$1
shift
M=$1
shift
idx=$*

$JSALTsrc/C/generate_pairs_from_idx --offset $offset $idx |
$JSALTsrc/C/killroy -N $N -M $M -tick 10000000

