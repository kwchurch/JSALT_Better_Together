#!/bin/sh

tmpdir=new_pairs_to_bigrams.$$
mkdir -p $tmpdir
$JSALTsrc/C/unprint_bigrams < $1 > $tmpdir/bigrams;
$JSALTsrc/C/sort_bigrams $tmpdir/bigrams | $JSALTsrc/C/uniq_bigrams --max > $1.bigrams

rm -rf $tmpdir

