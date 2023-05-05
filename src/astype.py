#!/usr/bin/env python

import os,sys,scipy.sparse,argparse,time
import numpy as np

t0 = time.time()

parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--input", required=True)
# parser.add_argument("-o", "--output", required=True)
# parser.add_argument("-N", "--N", type=int, default=None)
parser.add_argument("-B", "--block_size", type=int, default=1024)
parser.add_argument("-d", "--dtypes", help="from, to", required=True)
args = parser.parse_args()

dtypes = { 'int8' : np.int8,
           'int16' : np.int16,
           'int32' : np.int32,
           'int64' : int,
           'int' : int,
           'float16' : np.float16,
           'float32' : np.float32,
           'float64' : float,
           'float' : float}

for dt in args.dtypes.split(','):
    assert dt in dtypes, 'bad dtype arg: ' + dt

DT = [dtypes[dt] for dt in args.dtypes.split(',')]

with os.fdopen(sys.stdout.fileno(), 'wb', closefd=False) as stdout:
    with os.fdopen(sys.stdin.fileno(), 'rb', closefd=False) as stdin:
        while True:
            block = np.fromfile(stdin, dtype=DT[0], count=args.block_size)
            if len(block) == 0: break
            block2 = block.astype(DT[1])
            stdout.write(block2.tobytes())
            # block2.tofile(stdout)


