#!/usr/bin/env python

import os,sys,argparse,time
import numpy as np

t0 = time.time()

print('brute_force_cosines_kwc.py: ' + str(sys.argv), file=sys.stderr)
sys.stderr.flush()

apikey=os.environ.get('SPECTER_API_KEY')
parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("--N", type=int, help="number of corpus_ids to output", default=100)
parser.add_argument("--seed", type=int, help='set seet', default=None)
args = parser.parse_args()

print('seed: ' + str(args.seed), file=sys.stderr)

if not args.seed is None:
    np.random.seed(args.seed)

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def imap_to_dir(dir):
    fn = dir + '/map.new_to_old.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

ids = imap_to_dir(args.dir)
sample = np.random.choice(ids, args.N)

np.savetxt(sys.stdout, sample, fmt='%d')
