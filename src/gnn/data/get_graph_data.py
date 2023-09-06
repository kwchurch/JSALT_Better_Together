from utils import *
import numpy as np
import scipy 
import os 


def get_full_graph_in_coo():
    if not os.path.exists(f'{ROOT_DIR}/release-fullgraph/citations.row.npy'):
        print("Constructing COO graph")
        csr_graph = np.load(f'{ROOT_DIR}/release-fullgraph/citations.G.npz')
        indptr = csr_graph['indptr']
        indices = csr_graph['indices']
        csr = scipy.sparse.csr_array((np.zeros(indices.shape[0]), indices, indptr),\
                                    shape = (270 * 10 ** 6, 270 * 10 ** 6))
        coo = csr.tocoo()
        rows = coo.row
        cols = coo.col
        np.save(f'{ROOT_DIR}/release-fullgraph/citations.row', rows)
        np.save(f'{ROOT_DIR}/release-fullgraph/citations.col', cols)
    else: 
        print("Reading cached COO graph")
        rows  = np.load(f'{ROOT_DIR}/release-fullgraph/citations.row.npy')
        cols  = np.load(f'{ROOT_DIR}/release-fullgraph/citations.col.npy')
    return rows, cols 
    

def get_id2bins():
    id2bins = np.load(f'{ROOT_DIR}/id2bins.npy')
    return id2bins

