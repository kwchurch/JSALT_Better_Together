#!/usr/bin/env python

import sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
# parser.add_argument("-N", "--N", type=int, default=None)
# parser.add_argument("-d", "--dtype", default='int32')
# parser.add_argument("-K", "--hidden_dimensions", type=int, default=None)

args = parser.parse_args()

# dtypes = { 'int8' : np.int8,
#            'int16' : np.int16,
#            'int32' : np.int32,
#            'int64' : int,
#            'int' : int,
#            'float16' : np.float16,
#            'float32' : np.float32,
#            'float64' : float,
#            'float' : float}

# assert args.dtype in dtypes, 'bad dtype arg: ' + args.dtype

# X = np.fromfile(args.input, dtypes[args.dtype])
X = np.load(args.input).reshape(-1)

# if not args.hidden_dimensions is None:
#     X = X.reshape(-1, args.hidden_dimensions)

print(str(time.time() - t0) + ' loaded X', file=sys.stderr)
sys.stderr.flush()

X.tofile(args.output)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
