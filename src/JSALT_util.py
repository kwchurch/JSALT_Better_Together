
import numpy as np
import scipy

# faster than load_npz and save_npz, because there is no compression

def my_load_csr_matrix(prefix):
    data=np.load(prefix + '.data.npy')
    indices=np.load(prefix + '.indices.npy')
    indptr = np.load(prefix + '.indptr.npy')
    shape = np.load(prefix + '.shape.npy')
    format=np.load(prefix + '.format.npy')
    return scipy.sparse.csr_matrix((data, indices, indptr), shape=shape)

def my_save_csr_matrix(prefix, M):
    for i in M:
        np.save(prefix + '.' + i, M[i])



