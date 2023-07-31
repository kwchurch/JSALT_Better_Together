#!/usr/bin/env python

import sys,os,struct,argparse
import numpy as np

print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--bigrams", help="binary file", required=True)
parser.add_argument("--query", type=int, help="corpus id", default=None)
parser.add_argument('--ids_to_bins', help="a directory such as $JSALTdir/semantic_scholar/j.ortega/corpusId_to_bin.txt", default=None)
args = parser.parse_args()

def load_ids_to_bins():
    if args.ids_to_bins is None:
        return None
    if args.ids_to_bins.endswith('.npy'):
        return np.load(args.ids_to_bins)
    x = np.loadtxt(args.ids_to_bins).astype(int)
    nx = np.max(x[:,0]) + 1
    res = np.zeros(nx, dtype=np.int8)+100
    res[x[:,0]] = x[:,1]
    np.save(args.ids_to_bins + '.npy', res)
    return res

ids_to_bins = load_ids_to_bins()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def print_bigram(bytes):
    val,id1,id2 = struct.unpack('fii', bytes)
    if ids_to_bins is None:
        print('\t'.join(map(str, struct.unpack('fii', bytes))))
    else:
        val,id1,id2 = struct.unpack('fii', bytes)
        bin1 = ids_to_bins[id1]
        bin2 = ids_to_bins[id2]
        print('\t'.join(map(str, [val, id1, id2, bin1, bin2])))

if args.query is None:
    with open(args.bigrams, 'rb') as fd:
        while True:
            bytes = fd.read(12)
            if len(bytes) == 12:
                print_bigram(bytes)
                # print('\t'.join(map(str, struct.unpack('fii', bytes))))
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
            if ids_to_bins is None:
                print('\t'.join(map(str, record)))
            else:
                val,id1,id2 = record
                print('\t'.join(map(str, [val, id1, id2, bin1, bin2])))



        
    



