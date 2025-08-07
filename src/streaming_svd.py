#!/usr/bin/env python

# Let the input matrix, M, be a tall skinny matrix with shape (m, n)
# By tall skinny, we are assuming m >> n

# Assume M is normalized so rows have unit length
# In addition, assume rows of M are i.i.d.

# We are going to stream the matrix by reading batches of b rows
# where m >> b >> n

# The input matrix and the output matrix are stored as a sequence of
# floats (because they are big and we need to be able to stream them).
# The other matrices will be stores as numpy (.npy) matrices (because they are small).

# We will refer to n as hidden_dimensions.  That needs to be specified as an input argument.

# Thus, there are three output files:
#  args.output + '.U.f' (a sequence of np.float32 which can be reshaped as (m, n))
#  args.output + '.D.npy' (numpy matrix with shape: (n,))
#  args.output + '.Vt.npy' (numpy matrix with shape: (n, n))

# When we are done U @ D @ Vt should be close to normalize(M)

# Usage, create an input file
# X = np.random.random((30000,280)).astype(np.float32)
# X.tofile("/tmp/random.f")

# Run this program
# $JSALTsrc/streaming_svd.py  -i /tmp/random.f -o /tmp/random.f.svd -d 280 

# Read in M and compare M with MM
# where MM is reconstituted M

# from sklearn.preprocessing import normalize
# M  = normalize(np.fromfile('/tmp/random.f', dtype=np.float32).reshape(-1, 280))

# Reconstitute MM (should be close to M)
# U  = np.fromfile('/tmp/random.f.svd.U.f', dtype=np.float32).reshape(-1, 280)
# D = np.load("/tmp/random.f.svd.D.npy")
# Vt = np.load("/tmp/random.f.svd.Vt.npy")
# MM = U @ np.diag(D) @ Vt

# Verify that MM is close to M
# np.linalg.norm(M - MM)
# 0.00015830585

# Note that the nuclear norms of M and MM are close to one another
# np.linalg.norm(M, "nuc")
# 1593.7759
# np.linalg.norm(MM, "nuc")
# 1593.7762

# The method is based on the assumption
# that singular values scale a predictable way
# Let D0 be the singular values based on a sample (the size of a batch).
# Let D be the singular values of the final answer.
# We assume D approx sqrt(nB) * D0,
# where nB is the number of batches.
# This approximation is based on two assumptions:
#  (a) rows of M are i.i.d, and
#  (b) rows are unit length

# Related work:
# Google search on streaming svd returns a number of papers,
# though these papers are more complicated since
# they don't use the approximation above.

# https://arxiv.org/pdf/2108.08845
# https://arxiv.org/abs/2010.14226
# https://dspace.mit.edu/handle/1721.1/30429
# https://github.com/Romit-Maulik/PyParSVD
# https://github.com/pens/libssvd

# Here is a review of some of the work above (it was rejected)
# https://openreview.net/forum?id=4lLyoISm9M

# The review mentions some more references
# Yu, Gu, Li, Liu, Li, "Single-Pass PCA of Large High-Dimensional Data". IJCAI '17, https://doi.org/10.24963/ijcai.2017/468
# Ghashami, Liberty, Phillips, Woodruff, "Frequent directions: Simple and deterministic matrix sketching". SIAM Journal on Computing. 2016;45(5):1762-92.
# Martinsson, Tropp. "Randomized numerical linear algebra: Foundations and algorithms". Acta Numerica. 2020 May;29:403-572.

import numpy as np
import os,sys,argparse
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import randomized_svd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_floats", help="sequence of np.float32", required=True)
parser.add_argument("-d", "--hidden_dimensions", type=int, help="hidden dimensions", required=True)
parser.add_argument("-B", "--batch_size", type=int, help="split up the input floats into batches of rows (batch size defaults to 10k)", default=10000)
parser.add_argument("-o", "--output", help="pathname for output", required=True)
parser.add_argument("-V", '--verbose', action='store_true')
args = parser.parse_args()

fn_len = os.path.getsize(args.input_floats)
nrows = int(fn_len/(args.hidden_dimensions*4))
nbatches = int(nrows/args.batch_size)
M = np.memmap(args.input_floats, dtype=np.float32, shape=(nrows,args.hidden_dimensions), mode='r')

if len(M) <= args.batch_size:
    U,D,Vt = randomized_svd(normalize(M), n_components=M.shape[1])
    np.save(args.output + '.D.npy', D)
    np.save(args.output + '.Vt.npy', Vt0)
    U.astype(np.float32).tofile(args.output + '.U.f')
else:
    sample = M[np.random.choice(len(M), args.batch_size, replace=False),:]
    U0,D0,Vt0 = randomized_svd(normalize(sample), n_components=M.shape[1])

    # singular values scale with sqrt(nbatches)
    # Peter comment - the line requiring empirical or mathematic justification
    D = np.sqrt(nbatches) * D0
    Dinv = np.diag(1/D)

    if args.verbose:
        err = np.linalg.norm(np.eye(M.shape[1]) - Vt0 @ Vt0.T)
        print('Vt: err = %f' % (err))

    np.save(args.output + '.D.npy', D)
    np.save(args.output + '.Vt.npy', Vt0)

    # create an empty file
    open(args.output + '.U.f', 'wb').close()

    with open(args.output + '.U.f', 'ab') as Ufd:
        for i,batch in enumerate(range(nbatches)):
            Mi = normalize(M[batch * args.batch_size:(batch+1)* args.batch_size,:])
            UiRot = Mi @ Vt0.T @ Dinv
            UiRot.astype(np.float32).tofile(Ufd)
            
            if args.verbose:
                err = np.linalg.norm(Mi - UiRot @ np.diag(D) @ Vt0)
                print('batch %d: err = %f' % (i, err))

        # Need to do something special for the last batch (when nrows is not a multiple of batch_size)
        if len(M) > nbatches * args.batch_size:
            Mlast[-args.batch_size:,:]
            UlastRot = Mlast @ Vt0.T @ Dinv
            extraRows = nrows - nbatches * args.batch_size
            UiRot[-extraRows:,:].astype(np.float32).tofile(Ufd)


# More comments:

# Da : singular values of A
# Db : singular values of B
# Dab : singular values of A+B

# what are the singular values of A+B? what is Dab?

# if A and B are i.i.d samples of the same process
# and A and B have unit length
# then Dab approx sqrt(2) * Da approx sqrt(2) * Db

# but if A is a matrix of 0s (so it is not a sample of the same process)
# then A+B = B
# Da: vectors of 0s
# Db: something interesting
# Dab = Db (without the sqrt(2))

# reasonable assumptions: n >> b >> m
# where input matrix M has shape (n,m)
# tall skinny means n >> m


# combos rules
# 1. AB = A + B
# 2. AB = np.vstack([A, B])
# 3. AB = np.hstack([A, B])

# In all 3 cases, Dab approx sqrt(2) * Da approx sqrt(2) * Db

# Assume A.shape == B.shape
# Let zeros be a matrix of zeros with shape A.shape
# Let A' be np.vstack([A, zeros])
# and B' be np.vstack([zeros, B])

# Note, the singular values of zeros are 0

# Singular values are invariant to:
# 1. padding with zeros (either rows or columns)
# 2. swapping rows
# 3. swapping columns

# Note the singular values of A' are the same as the singular values of A
# and similarly, the singular values of B' are the same as the singular values of B

# Then singular values of np.stack([A, B]) = A' + B'
            
            
# more refs
# https://www.stat.uchicago.edu/~lekheng/courses/302/demmel/
# https://arxiv.org/pdf/2009.00761
