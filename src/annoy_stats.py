#!/usr/bin/env python

import numpy as np
from numpy import linalg
import gensim,sys,os,pickle,argparse,operator,time
from gensim.models import KeyedVectors
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity,euclidean_distances

t0 = time.time()

parser = argparse.ArgumentParser()
# default='/mnt/big/kwc/morphology/embedding_comparisons/annoys.txt'
parser.add_argument("-M", "--embedding", help="a filename or keyword in mapping_table", required=True)
parser.add_argument("-o", "--output", help="output file", required=True)
args = parser.parse_args()

def f2s(f):
    if f is None:
        return 'NA'
    else:
        return '%0.3f' % (f)
    
def floats2str(floats):
    return '|'.join([f2s(f) for f in floats])

def str2floats(str):
    return [ float(s) for s in str.split('|') ]

def vocab_from_annoy(M):
    return [k for k in M.vocab.__iter__()]

def i2s(i):
    if i is None:
        return 'NA'
    else:
        return str(i)

def ints2str(ints):
    return '|'.join([i2s(i) for i in ints])

M = gensim.models.KeyedVectors.load(args.embedding, mmap='r')
# V = vocab_from_annoy(M)

print(str(time.time() - t0) + ' finished loading M with M.vectors.shape: ' + str(M.vectors.shape), file=sys.stderr)
sys.stderr.flush()

l0 = np.linalg.norm(M.vectors, axis=0)

print(str(time.time() - t0) + ' finished axis 0', file=sys.stderr)
sys.stderr.flush()

l1 = np.linalg.norm(M.vectors, axis=1)

print(str(time.time() - t0) + ' finished axis 1', file=sys.stderr)
sys.stderr.flush()

np.savez(args.output, l0=l0, l1=l1)
print(str(time.time() - t0) + ' done', file=sys.stderr)

