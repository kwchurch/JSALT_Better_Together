#!/usr/bin/env python

import numpy as np
from numpy import linalg
# import pandas as pd
import sys,time,pdb,argparse,pickle,scipy,random,math
from scipy.sparse.linalg import svds, eigs, inv
# import matplotlib.pyplot as plt
from scipy import sparse

parser = argparse.ArgumentParser()
# parser.add_argument("-K", "--internal_dimensions", type=int, help="number of internal dimensions (typically 200)", required=True)
# parser.add_argument("-k", "--svd_dimensions", type=int, help="number of dimensions to do for inverted AAA matrix (typically 200)", required=True)
parser.add_argument("-V", "--vocabulary_size", type=int, help="vocabulary size (typically 10k)", required=True)
# parser.add_argument("-C", "--classes", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
# parser.add_argument("-c", "--classes_low", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
# parser.add_argument("-C", "--classes_high", type=int, help="classes (typically V/2 or V/3 or V/100)", required=True)
# parser.add_argument("-n", "--nclasses", type=int, help="number of classes (typically 10)", required=True)
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

# n=args.nclasses
# K=args.internal_dimensions
V=args.vocabulary_size

primes = [ i for i in range(V) if primep(i) ]

print(primes)



def AAapprox_inverse(l, C, V):
    """
    Arguments:
        l (float): Lambda.
        C (float): Constant to estimate the AA matrix.
        V (int or float): Vocab size.

    Returns:
        The inverse of (lambda * I + C) which is

            (1 / lambda) * I -
            (C / (lambda * (lambda + C * V)))
    """
    return np.eye(V) / l - (C / l / (l + C * V))
    #return 1 / l, -(C / l / (l + C * V))



def normalize(vec):
    l = linalg.norm(vec)
    if l == 0:
        return vec
    else:
        return vec/l

def normalize_len(m):
    l = linalg.norm(m, axis=1)
    for i in range(m.shape[0]):
        if l[i] != 0:
            m[i,:] = m[i,:]/l[i]
    return m            

# generate gold data
# this is the V by K answer we want to get to eventually
# but we have to start from n C by K matrices
# each of the C by K matrices are created by summing rows from the gold matrix.
# That is, Ai*gold (aka AM)
def new_gold(V, K):
    return normalize_len(np.array([ random.uniform(-1,1) for x in range(V*K)]).reshape((V,K)))

# Create a vector of length V that maps word i to a class
# The different iterations should do this in different ways
# So there are the same number of words in each class,
# and if we intersect two classes on two iterations, there is at most one word in the intersection
def word2class(V, C, iteration):
    res = np.zeros(V, dtype=np.int)
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

def new_Ai(V, C, iteration):
    vocab = range(V)
    # words_per_class = max(2, math.floor(V/C))
    word2class = new_word2class(V, C, iteration)
    inv = invert_word2class(word2class)
    alphas = [ 1/math.sqrt(len(inv[word2class[i]])) for i in range(len(word2class)) ]
    return sparse.csr_matrix((alphas, (word2class, vocab)), shape=(C, V))

def C2V(M, word2class):
    res = np.zeros((len(word2class), M.shape[1]), dtype=np.float)
    for i in range(len(word2class)):
        res[i,:] = M[word2class[i],:]
    return res

# R.dot(A) = B
# A.T.dot(R.T) = B.T (same as above)
def compute_left_rotation(A, B):
    U,s,V = np.linalg.svd(B.dot(A.T))
    return U.dot(V)

# A.dot(R) = B
def compute_right_rotation(A, B):
    return compute_left_rotation(A.T, B.T).T


def cos_score(v1, v2):
    d0=v1.shape[0]
    d1=v1.shape[1]
    return np.array([ v1[i,:].reshape(d1).T.dot(v2[i,:].reshape(d1)) for i in range(d0)])

def do_it(C):
    if C < 2 or C >= V:
        return
    # pdb.set_trace()
    M=gold=new_gold(V,K)
    As = [ new_Ai(V, C, i) for i in range(n)]
    AM = [ normalize_len(Ai.dot(M)) for Ai in As ]
    word2classes = [ new_word2class(V, C, i) for i in range(n) ]
    inverted = [invert_word2class(w2c) for w2c in word2classes]
    gold_scores = [ cos_score(gold, C2V(AM[i], word2classes[i])) for i in range(n) ]
    class_scores = [ cos_score(AM[i], AM[i+1]) for i in range(n-1) ]
    words_per_class = max(2, V/C)
    M=gold
    AM = [ Ai.dot(M) for Ai in As ]
    AtM = sum([ As[i].T.dot(AM[i]) for i in range(n) ])/n
    reg = args.regularizing_constant
    AAsparse = sum([Ai.T.dot(Ai) for Ai in As])/n
    AAA = reg * scipy.sparse.eye(V) + AAsparse
    t1 = time.time()
    AA = linalg.inv(scipy.sparse.csr_matrix.todense(AAA))
    M = np.squeeze(np.asarray(normalize_len(AA.dot(AtM))))
    inv_time = time.time() - t1
    AAapprox = AAapprox_inverse(reg, C, V)
    Mapprox = np.squeeze(np.asarray(normalize_len(AAapprox.dot(AtM))))
    M_without_Z = np.squeeze(np.asarray(normalize_len(AtM)))

    # spsolve(A, b[, permc_spec, use_umfpack])	Solve the sparse linear system Ax=b, where b may be a vector or a matrix.
    t1 = time.time()
    M2 = scipy.sparse.linalg.spsolve(AAA, AtM)
    solve_time = time.time() - t1

    s1 = np.mean(cos_score(M, gold))
    s2 = np.mean(cos_score(Mapprox, gold))
    s3 = np.mean(cos_score(M_without_Z, gold))
    print('%f\t%f\t%f\t%d\t%d\t%d\t%d\t%f' % (# time.time() - t0, inv_time, solve_time, 
        s1, s2, s3, V, C, K, n, reg))

print('gain\tgain_with_approx\tgain_without_Z\tV\tC\tK\tn\tlambda')    
for C in primes:
    # print('C = %d' % (C))
    do_it(C)
