import numpy as np
import scipy
from scipy import sparse, linalg
from sklearn import preprocessing
from sklearn.utils.extmath import randomized_svd
from datetime import datetime
import os

# added by kwc
import sys,time

from nodevectors.embedders import BaseNodeEmbedder
import csrgraph as cg

class ProNE(BaseNodeEmbedder):
    def __init__(self, n_components=32, step=10, mu=0.2, theta=0.5, 
                exponent=0.75, verbose=True, save_svd=False, load_svd=False, svd_file="."):
        """
        Fast first order, global method.

        Embeds by doing spectral propagation over an initial SVD embedding.
        This can be seen as augmented spectral propagation.

        Parameters :
        --------------
        step : int >= 1
            Step of recursion in post processing step.
            More means a more refined embedding.
            Generally 5-10 is enough
        mu : float
            Damping factor on optimization post-processing
            You rarely have to change it
        theta : float
            Bessel function parameter in Chebyshev polynomial approximation
            You rarely have to change it
        exponent : float in [0, 1]
            Exponent on negative sampling
            You rarely have to change it
        References:
        --------------
        Reference impl: https://github.com/THUDM/ProNE
        Reference Paper: https://www.ijcai.org/Proceedings/2019/0594.pdf
        """
        self.n_components = n_components
        self.step = step
        self.mu = mu
        self.theta = theta
        self.exponent = exponent
        self.verbose = verbose
        self.save_svd = save_svd
        self.load_svd = load_svd
        self.svd_file = svd_file

    # kwc added: features_matrix arg
    def fit_transform(self, graph, features_matrix=None):
        """
        NOTE: Currently only support str or int as node name for graph
        Parameters
        ----------
        nxGraph : graph data
            Graph to embed
            Can be any graph type that's supported by CSRGraph library
            (NetworkX, numpy 2d array, scipy CSR matrix, CSR matrix components)
        """

        t0 = time.time()        # added by kwc

        G = cg.csrgraph(graph)

        t1 = time.time()        # added by kwc
        
        if features_matrix is None:
            features_matrix = self.pre_factorization(G.mat,
                                                     self.n_components,
                                                     self.exponent,self.save_svd, self.load_svd, self.svd_file)
            t2 = time.time()        # added by kwc
        else:
            t2 = time.time()        # added by kwc

        vectors = ProNE.chebyshev_gaussian(
            G.mat, features_matrix, self.n_components,
            step=self.step, mu=self.mu, theta=self.theta)

        t3 = time.time()        # added by kwc

        self.model = dict(zip(G.nodes(), vectors))

        t4 = time.time()        # added by kwc

        return vectors
    
    def fit(self, graph):
        """
        NOTE: Currently only support str or int as node name for graph
        Parameters
        ----------
        nxGraph : graph data
            Graph to embed
            Can be any graph type that's supported by CSRGraph library
            (NetworkX, numpy 2d array, scipy CSR matrix, CSR matrix components)
        """

        t0 = time.time()        # added by kwc

        G = cg.csrgraph(graph)

        t1 = time.time()        # added by kwc

        features_matrix = self.pre_factorization(G.mat,
                                                 self.n_components, 
                                                 self.exponent,
                                                 self.save_svd, self.load_svd, self.svd_file)

        t2 = time.time()        # added by kwc

        vectors = ProNE.chebyshev_gaussian(
            G.mat, features_matrix, self.n_components,
            step=self.step, mu=self.mu, theta=self.theta)

        t3 = time.time()        # added by kwc

        self.model = dict(zip(G.nodes(), vectors))

    @staticmethod
    def tsvd_rand(matrix, n_components, save_svd, load_svd, svd_file):
        """
        Sparse randomized tSVD for fast embedding
        """


        l = matrix.shape[0]
        # Is this csc conversion necessary?
        t0 = time.time()        # added by kwc
        smat = sparse.csc_matrix(matrix)
        t1 = time.time()        # added by kwc
        if load_svd:
            # added by jeo
            U = None
            U = np.load(svd_file)
        else:
            t2 = time.time()        # added by kwc
            #import dask
            #dask.config.set({"optimization.fuse.ave-width": 5})
            #import dask.array as da
            #da.config.set({"optimization.fuse.ave-width": 5})
            U, Sigma, VT = randomized_svd(smat, 
                n_components=n_components, 
                n_iter=5, random_state=None)
            #U, Sigma, VT = da.linalg.svd_compressed(smat, k=10, compute=True)
            #U, Sigma, VT = da.linalg.svd_compressed(smat,n_power_iter=5, k=n_components, compute=True)
            #smat = smat[5000:]
            #smat = smat[1:5000, 1:5000]
            #smat = smat[0:5000, :]
            #x = da.from_array(smat, chunks=(100, 100))
            #x = da.from_array(smat, chunks=(1000, 1000))
            #x = da.from_array(smat, chunks=(100000, 100000))
            #U, Sigma, VT = da.linalg.svd_compressed(smat, k=n_components, compute=True)
            #U, Sigma, VT = da.linalg.svd_compressed(x, k=n_components, compute=True)
            #VT.compute()


            t3 = time.time()        # added by kwc
            # added by kwc
            U = U * np.sqrt(Sigma)
            U = preprocessing.normalize(U, "l2")
            if save_svd:
                if not os.path.exists(svd_file):
                    os.makedirs(svd_file)
                    numpy_file = svd_file + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3] + ".npy"
                    np.save(numpy_file, U)
        return U
    @staticmethod
    def pre_factorization(G, n_components, exponent, save_svd, load_svd, svd_file):
        """
        Network Embedding as Sparse Matrix Factorization
        """
        C1 = preprocessing.normalize(G, "l1")
        # Prepare negative samples
        neg = np.array(C1.sum(axis=0))[0] ** exponent
        neg = neg / neg.sum()
        neg = sparse.diags(neg, format="csr")
        neg = G.dot(neg)
        # Set negative elements to 1 -> 0 when log
        C1.data[C1.data <= 0] = 1
        neg.data[neg.data <= 0] = 1
        C1.data = np.log(C1.data)
        neg.data = np.log(neg.data)
        C1 -= neg
        features_matrix = ProNE.tsvd_rand(C1, n_components=n_components, save_svd=save_svd, load_svd=load_svd, svd_file=svd_file)
        return features_matrix

    @staticmethod
    def svd_dense(matrix, dimension):
        """
        dense embedding via linalg SVD
        """
        t0 = time.time()        # added by kwc
        U, s, Vh = linalg.svd(matrix, full_matrices=False, 
                              check_finite=False, 
                              overwrite_a=True)
        t1 = time.time()        # added by kwc
        U = np.array(U)
        U = U[:, :dimension]
        s = s[:dimension]
        s = np.sqrt(s)
        U = U * s
        t2 = time.time()        # added by kwc
        U = preprocessing.normalize(U, "l2")
        t3 = time.time()        # added by kwc
        return U

    @staticmethod
    def chebyshev_gaussian(G, a, n_components=32, step=10, 
                           mu=0.5, theta=0.5):
        """
        NE Enhancement via Spectral Propagation

        G : Graph (csr graph matrix)
        a : features matrix from tSVD
        mu : damping factor
        theta : bessel function parameter
        """
        
        t0 = time.time()        # added by kwc
        nnodes = G.shape[0]
        if step == 1:
            return a
        A = sparse.eye(nnodes) + G
        DA = preprocessing.normalize(A, norm='l1')
        # L is graph laplacian
        L = sparse.eye(nnodes) - DA
        M = L - mu * sparse.eye(nnodes)
        Lx0 = a
        Lx1 = M.dot(a)
        Lx1 = 0.5 * M.dot(Lx1) - a
        conv = scipy.special.iv(0, theta) * Lx0
        conv -= 2 * scipy.special.iv(1, theta) * Lx1
        t1 = time.time()        # added by kwc
        
        
        # Use Bessel function to get Chebyshev polynomials
        for i in range(2, step):
            t2 = time.time()        # added by kwc
            Lx2 = M.dot(Lx1)
            Lx2 = (M.dot(Lx2) - 2 * Lx1) - Lx0
            
            if i % 2 == 0:
                conv += 2 * scipy.special.iv(i, theta) * Lx2
            else:
                conv -= 2 * scipy.special.iv(i, theta) * Lx2
            Lx0 = Lx1
            Lx1 = Lx2
            del Lx2
            t3 = time.time()        # added by kwc
        
        
        mm = A.dot(a - conv)
        t4 = time.time()        # added by kwc
        emb = ProNE.svd_dense(mm, n_components)
        t5 = time.time()        # added by kwc
        return emb
