#!/usr/bin/env python

import os,sys,argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("--direction", help="old_to_new|new_to_old", required=True)
parser.add_argument("--input", help="input file (seq of int32)", default=None)
parser.add_argument("--output", help="output file (seq of int32)", default=None)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def my_int(s):
    for i,c in enumerate(s):
        if not c.isdigit():
            return int(s[0:i])

def record_size_from_dir(dir):
    with open(dir + '/record_size', 'r') as fd:
        return my_int(fd.read())

def map_from_dir(dir):
    fn = dir + '/map.' + args.direction + '.i'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def embedding_from_dir(dir, K):
    fn = dir + '/embedding.f'
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.float32, shape=(int(fn_len/(4*K)), K), mode='r')

def directory_to_config(dir):
    K = record_size_from_dir(dir)
    return { 'record_size' : K,
             'dir' : dir,
             'map' : map_from_dir(dir),
             # 'embedding' : embedding_from_dir(dir, K)
    }

config = directory_to_config(args.dir)

if args.input is None:
    for line in sys.stdin:
        if len(line) > 0:
            id_in = int(line)
            id_out = -1
            if id_in >= 0 and id_in < len(config['map']):
                id_out = config['map'][id_in]
            print(str(id_out))
else:
    assert not args.output is None, '--output must be specified if --input is specified'
    X = map_int32(args.input)
    Y = config['map'][X]
    Y.tofile(args.output)

                
