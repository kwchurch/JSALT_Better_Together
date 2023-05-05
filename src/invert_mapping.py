#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-M", "--mapping", help=".new_to_old.i file", required=True)
args = parser.parse_args()

assert args.mapping.endswith('.new_to_old.i'), 'bad mapping file'

with open(args.mapping, 'rb') as fd:
    new_to_old = np.frombuffer(fd.read(), dtype=np.int32)

old_to_new = np.zeros(1+max(new_to_old), dtype=np.int32) -1
old_to_new[new_to_old] = np.arange(len(new_to_old), dtype=np.int32)

outfile = args.mapping[0:-(len('.new_to_old.i'))] + '.old_to_new.i'

old_to_new.tofile(outfile)






