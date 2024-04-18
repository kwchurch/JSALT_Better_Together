#!/bin/sh

xy=$1;
shift

cat $*  | $JSALTsrc/C/x_to_y $xy 
