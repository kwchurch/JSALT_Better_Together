#!/usr/bin/env python

import sys,scipy.sparse,time,argparse
import numpy as np
import random

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
parser.add_argument("-K", '--n_components', type=int, default=100)
parser.add_argument("-R", "--report", type=int, help="interval for reporting progress", default=10)
parser.add_argument("-S", "--seed", type=int, default=42)
parser.add_argument("-p", "--pieces", type=int, help="split output into this many files", default=400)
args = parser.parse_args()

np.random.seed(args.seed)

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)

print(str(time.time() - t0) + ' finished loading M; shape: ' + str(M.shape), file=sys.stderr)
sys.stderr.flush()

if args.transpose:
    M = M.T
else:
    M = scipy.sparse.csc_matrix(M, dtype=M.dtype, shape=M.shape)

print(str(time.time() - t0) + ' finished transposing: args.transpose = ' + str(args.transpose), file=sys.stderr)
sys.stderr.flush()

fanout = np.sum(M, axis=1)      # just changed this from axis=0

print(str(time.time() - t0) + ' finished computing fanout', file=sys.stderr)
sys.stderr.flush()


N=M.shape[1]
# idx = np.arange(N, dtype=np.int32)
# P = np.random.permutation(N)
# Pinv = np.zeros(N, dtype=np.int32)
# Pinv[P] = idx
# idx = None                      # free up space

# print(str(time.time() - t0) + ' finished creating permutation', file=sys.stderr)
# sys.stderr.flush()

# fanout = np.sum(M, axis=1)      # just changed this from axis=0

# This takes almost 10 minutes; not sure why
# I think the mistake was to use sum instead of np.sum
# see https://stackoverflow.com/questions/10922231/pythons-sum-vs-numpys-numpy-sum

# big = np.array(fanout > args.n_components).reshape(-1)
# nbig = sum(big)

big1 = fanout > args.n_components
print(str(time.time() - t0) + ' finished computing big1', file=sys.stderr)
sys.stderr.flush()

big = np.array(big1).reshape(-1)
print(str(time.time() - t0) + ' finished computing big', file=sys.stderr)
sys.stderr.flush()

big1 = None                     # free up memory
nbig = np.sum(big)

print(str(time.time() - t0) + ' nbig = %d' % nbig, file=sys.stderr)
sys.stderr.flush()

# big = np.array([i for i in range(N) if fanout[0,i] >= args.n_components], dtype=int)

big_indexes = np.arange(N)[big]
# np.save(args.output + 'indexes', big_indexes)

print(str(time.time() - t0) + ' M has %d bytes for indices, %d bytes for indptr and %d bytes for data'  % (M.indices.nbytes,  M.indptr.nbytes,  M.data.nbytes), file=sys.stderr)

ibig_indexes = {}
for i,y in enumerate(big_indexes):
    if not y in ibig_indexes:
        ibig_indexes[y] = []
    ibig_indexes[y].append(i)

print(str(time.time() - t0) + ' finished inverting big indexes', file=sys.stderr)

# newM = M.copy()
# newM[big_indexes,:] = 0

# create a big empty matrix
# C0 = scipy.sparse.dok_matrix(M.shape, dtype=bool)

# This allocates too much memory
# C0[big_indexes,:] = M[big_indexes,:]

L = M[big_indexes,:]
print(str(time.time() - t0) + ' L has %d bytes for indices, %d bytes for indptr and %d bytes for data'  % (L.indices.nbytes,  L.indptr.nbytes,  L.data.nbytes), file=sys.stderr)

L.resize(M.shape)
print(str(time.time() - t0) + ' after resize, L has %d bytes for indices, %d bytes for indptr and %d bytes for data'  % (L.indices.nbytes,  L.indptr.nbytes,  L.data.nbytes), file=sys.stderr)

newM = M - L # newM has the small rows (rows with no more than K nonzeros)
L = None    # free up memory
print(str(time.time() - t0) + ' newM has %d bytes for indices, %d bytes for indptr and %d bytes for data'  % (newM.indices.nbytes,  newM.indptr.nbytes,  newM.data.nbytes), file=sys.stderr)

# E = M.count_nonzero()
# newE = newM.count_nonzero()
# print(str(time.time() - t0) + ' E = %d; small E = %d; delta = %d' % (E, newE, E-newE), file=sys.stderr)
# sys.stderr.flush()


scipy.sparse.save_npz('%s.small' % (args.output), newM)

print(str(time.time() - t0) + ' finished saving small', file=sys.stderr)
sys.stderr.flush()

newM = None                     # free up memory

# newM = M[big,:]
# newM = M
# scipy.sparse.save_npz(args.output, newM)

def ksmallest(vals, k):
    n = len(vals)
    if n < 2*k:
        return sorted(vals)[0:k]
    else:
        lo = np.min(vals)
        hi = np.max(vals)
        r = hi - lo
        mid = lo + (1.1 * r)/k
        s = vals < mid
        if sum(s) >= k:
            return ksmallest(vals[s], k)
        else:
            return sorted(vals)[0:k]

pieces = np.random.choice(args.pieces, nbig)
print(str(time.time() - t0) + ' finished assigning pieces ', file=sys.stderr)
sys.stderr.flush()

t0a = time.time()
for p in range(args.pieces):
    # indexes = big_indexes[pieces == p]
    indexes = ibig_indexes[p]
    newM = M[indexes,:]
    scipy.sparse.save_npz('%s.%03d' % (args.output, p), newM)

    # print(str(time.time() - t0) + ' finished saving piece ' + str(p), file=sys.stderr)
    if p == 0: continue        
    t1 = time.time() - t0a
    i = p
    print('i = %d of %d, sec = %f, i per sec = %f, ETA = %f' % (i, args.pieces, t1, i/t1, (args.pieces * t1/i - t1)), file=sys.stderr)
    sys.stderr.flush()


# t0a = time.time()

# X2s = []
# Y2s = []
# for i,v in enumerate(big_indexes):

#     assert v < newM.shape[0], 'cannot find v = %d in newM' % v

#     _,Y = newM[v,:].nonzero()

#     assert len(Y) > args.n_components, 'expected at least %d nonzero values, but found just %d (i=%d)' % (args.n_components, len(Y), i)
    
#     X2 = np.zeros(args.n_components, dtype=np.int32) + v
#     X2s.append(X2)
    
#     Y2 = Pinv[ksmallest(P[Y], args.n_components)]
#     Y2s.append(Y2)

#     if i>0 and i%args.report == 0:
#         t1 = time.time() - t0a
#         print('i = %d of %d, sec = %f, i per sec = %f, ETA = %f' % (i, nbig, t1, i/t1, (nbig * t1/i - t1)), file=sys.stderr)
#         sys.stderr.flush()

# X = np.concatenate(X2s)
# Y = np.concatenate(Y2s)
# V = np.ones(len(X), dtype=bool)
# bigSketch = scipy.sparse.csr_matrix((V, (X, Y)), dtype=bool, shape=newM.shape)

# scipy.sparse.save_npz(args.output + '.sketch', bigSketch)

# def sketch(row):
#     res = scipy.sparse.lil_matrix((1,N), dtype=bool)
#     _,Y = row.nonzero()
#     Ps = P[Y]
#     pairs = sorted([ (p,y) for p,y in zip(Ps,Y)], key = lambda pair: pair[0])[0:args.n_components]
#     for p,y in pairs:
#         row[0,y]=1
#     return res

# S = scipy.sparse.lil_matrix(M.shape, dtype=bool)



# print(str(time.time() - t0) + ' starting crux', file=sys.stderr)
# sys.stderr.flush()

# for i in range(N):
#     if i>0 and i%args.report == 0:
#         t1 = time.time() - t0
#         print('i = %d of %d, sec = %f, i per sec = %f, ETA = %f' % (i, N, t1, i/t1, (N * t1/i - t1)), file=sys.stderr)
#         sys.stderr.flush()
#     f = fanout[0,i]
#     if f <= 0: continue
#     if f < args.n_components:
#         S[i,:] = M[i,:]
#     else:
#         print('about to call sketch on i: %s with f: %d ' % (i, f), file=sys.stderr)
#         sys.stderr.flush()
#         S[i,:] = sketch(M[i,:])

# print(str(time.time() - t0) + ' finished crux', file=sys.stderr)
# sys.stderr.flush()

# S = scipy.sparse.csr_matrix(S, dtype=bool)

# print(str(time.time() - t0) + ' saving results', file=sys.stderr)
# sys.stderr.flush()

# scipy.sparse.save_npz(args.output, S)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
