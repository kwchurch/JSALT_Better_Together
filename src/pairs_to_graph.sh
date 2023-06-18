#!/bin/sh

pairs=$1
T=$2
tmpdir=$1.tmpdir.$$
mkdir -p $tmpdir


awk '$1 > T' T=$T $pairs > $tmpdir/pairs 
cut -f1 < $tmpdir/pairs | $JSALTsrc/x_to_y af > $tmpdir/pairs.f
cut -f2 < $tmpdir/pairs | $JSALTsrc/x_to_y ai > $tmpdir/pairs.X.i
cut -f3 < $tmpdir/pairs | $JSALTsrc/x_to_y ai > $tmpdir/pairs.Y.i

$JSALTsrc/pairs_to_graph.py --input $tmpdir/pairs --output $pairs.npz

rm -rf $tmpdir
