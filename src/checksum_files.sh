#!/bin/sh

for f in $*
do
cksum $f > $f.cksum
done
