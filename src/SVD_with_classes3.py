#!/usr/bin/env python

import pdb

import numpy as np

import sys,time,argparse,scipy,math
# from scipy.sparse.linalg import svds, eigs, inv
# from scipy import sparse
import sklearn.preprocessing

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

# w2c = np.array([np.random.choice(V, size=C) for i in range(n)])

def assign(V, C):
    Ac = np.arange(C)
    res = np.array([Ac for i in range(math.ceil(V/C))]).reshape(-1)
    # np.random.shuffle(res)
    return res[0:V]

def my_rotate(vec, i):
    if i >= 0 and i < len(vec):
        return np.concatenate((vec[i:] , vec[:i]))
    else:
        vec2 = np.copy(vec)
        np.random.shuffle(vec2)
        return vec2

A1 = assign(V,C)
# w2c = np.array([my_rotate(A1,p) for p in primes[0:n]]).T

# w2c = np.random.choice(C, size=(V,n))

# np.savetxt(sys.stdout, w2c , fmt='%d')


def Ai(w2c):
    vals = np.ones(len(w2c))
    mat = scipy.sparse.csr_matrix((vals, (w2c, np.arange(V))))
    return sklearn.preprocessing.normalize(mat)

Ais = [Ai(my_rotate(A1,p)) for p in primes[0:n]]

pdb.set_trace()
