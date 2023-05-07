#!/bin/sh

embeddingDir=$1

JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

$JSALTsrc/C/near_with_floats --dir $embeddingDir $embeddingDir/idx.*.i |
cut -f1-3  | sort -nr -u

