#!/bin/sh

cut -f1,2 | pairs_to_cos --map $map --floats $ffile --record_size $K

