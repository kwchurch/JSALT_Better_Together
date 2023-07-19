#!/bin/sh

$JSALTsrc/C/sort_bigrams -m $* | $JSALTsrc/C/uniq_bigrams --max 
