#!/usr/bin/env python

import numpy as np

import sys,time,pdb,argparse,pickle,scipy,random,math
from scipy.sparse.linalg import svds, eigs, inv
from scipy import sparse

parser = argparse.ArgumentParser()
# parser.add_argument("-K", "--internal_dimensions", type=int, help="number of internal dimensions (typically 200)", required=True)
# parser.add_argument("-k", "--svd_dimensions", type=int, help="number of dimensions to do for inverted AAA matrix (typically 200)", required=True)
parser.add_argument("-V", "--vocabulary_size", type=int, help="vocabulary size (typically 10k)", required=True)
parser.add_argument("-C", "--classes", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
# parser.add_argument("-c", "--classes_low", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
# parser.add_argument("-C", "--classes_high", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
parser.add_argument("-n", "--nclasses", type=int, help="number of classes (typically 10)", required=True)
# parser.add_argument("-L", "--regularizing_constant", type=float, default=1e-3, help="regularizing constant")
args = parser.parse_args()

def primep(a):
    if a < 4:
        return 1
    k=0
    for i in range(2,a//2+1):
        if(a%i==0):
            return 0
    return 1

n=args.nclasses
# K=args.internal_dimensions
V=args.vocabulary_size
C=args.classes

primes = [ i for i in range(V) if primep(i) ]

def word2class(V, C, iteration):
    res = np.zeros(V, dtype=int)
    words_per_class = max(2, math.ceil(V/C))
    for i in range(C):
        for j in range(words_per_class):
            o = (i+j*C)
            p = primes[-1]
            if j < len(primes):
                p = primes[j]
            if o < V:
                res[o] = (i + p*iteration) % C
    return res

def invert_word2class(w2c):
    res = {}
    for i in range(len(w2c)):
        v = w2c[i]
        if not(v in res):
            res[v]=[]
        res[v].append(i)
    return res

def prime_near(x):
    for i,p in enumerate(primes):
        if p > x:
            return primes[i-1]
    return primes[-1]
            

# Vprime = prime_near(V)
# Cprime = prime_near(C)

# print('# V = %d, Vprime = %d, C = %d, Cprime = %d' % (V, Vprime, C, Cprime))

w2c = np.array([word2class(V, C, i) for i in range(n)])

np.savetxt(sys.stdout, w2c.T , fmt='%d')

# for i in range(n):
#     print('i = %d' % i)
#     w2c = word2class(V, C, i)
#     print('# assignments')
#     print(w2c)

#     print('#bincount')
#     print(np.bincount(w2c))
