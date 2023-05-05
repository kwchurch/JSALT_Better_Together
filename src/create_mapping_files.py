#!/usr/bin/env python

import sys,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help=".npz file", required=True)
args = parser.parse_args()

x = np.load(args.input)

x['old_to_new'].tofile(args.input + '.old_to_new.i')
x['new_to_old'].tofile(args.input + '.new_to_old.i')

print(str(time.time() - t0) + ' create_mapping_files: done', file=sys.stderr)
sys.stderr.flush()
