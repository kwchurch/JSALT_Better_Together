#!/bin/sh

T=$1
out=$2
bigrams=$3

$JSALTsrc/C/bigrams_to_XY_data $T $out.X $out.Y < $bigrams
$JSALTsrc/graph_fromfile.py -i $out -N 270000000 -o $bigrams.npz

