#!/usr/bin/env python

import sys,os,struct,argparse
import numpy as np

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--bigrams", help="binary file", required=True)
parser.add_argument("--query", type=int, help="corpus id", default=None)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

if args.query is None:
    with open(args.bigrams, 'rb') as fd:
        while True:
            bytes = fd.read(12)
            if len(bytes) == 12:
                print('\t'.join(map(str, struct.unpack('fii', bytes))))
            else:
                sys.exit(0)

else:
    idx = map_int64(args.bigrams + '.idx')
    start = idx[args.query]
    end = idx[args.query+1]
    nbytes = 12*(end - start)
    with open(args.bigrams, 'rb') as fd:
        fd.seek(start * 12)
        bytes = fd.read(nbytes)
        for record in struct.iter_unpack('fii', bytes):
            print('\t'.join(map(str, record)))


        
    



