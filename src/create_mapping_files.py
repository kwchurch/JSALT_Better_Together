#!/usr/bin/env python

import sys,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help=".npz file or text file", required=True)
args = parser.parse_args()

try:
    x = np.load(args.input)
    x['old_to_new'].tofile(args.input + '.old_to_new.i')
    x['new_to_old'].tofile(args.input + '.new_to_old.i')
except:
    new_to_old = np.loadtxt(args.input, dtype=np.int32)
    new_to_old.tofile(args.input + '.new_to_old.i')
    N = np.max(new_to_old)+1
    old_to_new = np.zeros(N, dtype=np.int32) -1
    for i,v in enumerate(new_to_old):
        old_to_new[v] = i
    old_to_new.tofile(args.input + '.old_to_new.i')

print(str(time.time() - t0) + ' create_mapping_files: done', file=sys.stderr)
sys.stderr.flush()
