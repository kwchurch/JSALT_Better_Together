#!/usr/bin/env python


# Examples (with and without -G arg)
# # uses API until -G is provided

# echo 2 | $JSALTsrc/refs.py
# 2	71	1479538, 46470924, 4430392, 15036950, 207741897, 34299859, 925588, 1441710, 18355475, 39380342, 41476623, 31242316, 37639608, 1345193, 118901444, 3188049, 6306536, 43353376, 420970, 15455464, 11409876, 30837181, 16190154, 89141, 189866725, 62657762, 21864171, 120933989, 153546381, 54174771, 14899020, 2625643, 16596643, 58942889, 140109802, 3772657, 207579947, 1609914, 683036, 5885617, 13463620, 930676, 153847808, 18547380, 6863121, 38936833, 207547900, 120760685, 207738357, 1836349, 27026167, 667586, 18718011, 5262555, 6530745, 153931876, 21877334, 9166388, 154137886, 58180322, 58068920, 28637672, 125133067, 167485681, 177751, 57229593, 117986589, 15829331, 14301809, None, None


# G=$JSALTdir/semantic_scholar/releases/2023-05-09/database/citations/graphs/citations.G
# echo 2 | $JSALTsrc/refs.py -G $G
# 2	62	177751, 420970, 667586, 683036, 925588, 930676, 1345193, 1441710, 1479538, 1836349, 2625643, 3188049, 3772657, 4430392, 5262555, 5885617, 6306536, 6530745, 6863121, 11409876, 13463620, 14301809, 14899020, 15036950, 15455464, 15829331, 16190154, 16596643, 18355475, 18547380, 18718011, 21877334, 27026167, 28637672, 30837181, 31242316, 34299859, 37639608, 38936833, 39380342, 41476623, 43353376, 46470924, 54174771, 57229593, 58180322, 62657762, 117986589, 118901444, 120760685, 120933989, 125133067, 140109802, 153546381, 153847808, 153931876, 154137886, 167485681, 189866725, 207547900, 207579947, 207738357

import json,requests,argparse
import os,sys,argparse,time
import numpy as np

t0 = time.time()

print('refs: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help="file (without .X.i and .Y.i)", default=None)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

Y = idx = None

if not args.graph is None:
    Y = map_int32(args.graph + '.Y.i')

    if not os.path.exists(args.graph + '.X.i.idx'):
        print('%0.0f sec: computing idx' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        X = map_int32(args.graph + '.X.i')
        res = np.cumsum(np.bincount(X))
        res.tofile(args.graph + '.X.i.idx')
        print('%0.0f sec: idx computed' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

    idx = map_int64(args.graph + '.X.i.idx')

def extract_row(x):
    # print('extract_row: ' + str(x))
    if x >= len(idx) or x < 0:
        return []
    if x == 0:
        return Y[:idx[0]]
    else:
        return Y[idx[x-1]:idx[x]]

def my_int(s):
    for i,c in enumerate(s):
        if not c.isdigit():
            return int(s[0:i])

def get_corpusId(ref):
    try:
        return ref['externalIds']['CorpusId']
    except:
        return None

def id_to_references(my_id):

    if not args.graph is None:
        return extract_row(int(my_id))

    cmd = 'https://api.semanticscholar.org/graph/v1/paper/CorpusId:' + str(my_id) + '/?fields=references,references.externalIds'
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if 'references' in j and not j['references'] is None:
        return [ get_corpusId(ref) for ref in j['references']]
    else:
        return []

# ids = np.loadtxt(sys.stdin).astype(int)
for line in sys.stdin:
    id1 = line.rstrip()
    if len(id1) < 1: continue
    refs = id_to_references(id1)
    print('\t'.join([id1, str(len(refs)), ', '.join(map(str, refs))]))

print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
