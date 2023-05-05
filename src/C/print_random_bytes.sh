#!/bin/sh

ifile=$1
N=$2
idx=$ifile.idx.${SLURM_ARRAY_TASK_ID}

print_random_bytes_index $ifile $idx $N --binary > $idx.hamming_dist16





