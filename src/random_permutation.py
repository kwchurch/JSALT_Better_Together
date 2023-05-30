#!/usr/bin/env python

import sys,argparse
import numpy as np

print('random_permutation: ' + str(sys.argv), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-N", "--N", type=int, help="N", required=True)
parser.add_argument("-o", "--output", help="output file", required=True)
args = parser.parse_args()

p = np.random.permutation(int(args.N))
p.tofile(args.output)

