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
        print('%0.0f sec: ProNE starting' % (t1 - t0), file=sys.stderr)
        sys.stderr.flush()
        
        if features_matrix is None:
            features_matrix = self.pre_factorization(G.mat,
                                                     self.n_components,
                                                     self.exponent,self.save_svd, self.load_svd, self.svd_file)
            t2 = time.time()        # added by kwc
            print('%0.0f sec: ProNE pre_factorization' % (t2 - t0), file=sys.stderr)
        else:
            t2 = time.time()        # added by kwc
            print('%0.0f sec: using precomputed ProNE pre_factorization' % (t2 - t0), file=sys.stderr)
        sys.stderr.flush()

        vectors = ProNE.chebyshev_gaussian(
            G.mat, features_matrix, self.n_components,
            step=self.step, mu=self.mu, theta=self.theta)

        t3 = time.time()        # added by kwc
        print('%0.0f sec: ProNE chebyshev gaussian' % (t3 - t0), file=sys.stderr)
        sys.stderr.flush()

        self.model = dict(zip(G.nodes(), vectors))

        t4 = time.time()        # added by kwc
        print('%0.0f sec: ProNE finishing' % (t4 - t0), file=sys.stderr)
        sys.stderr.flush()

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
        print('%0.0f sec: jeo fit csrgraph create total' % (t1 - t0), file=sys.stderr)
        sys.stderr.flush()

        features_matrix = self.pre_factorization(G.mat,
                                                 self.n_components, 
                                                 self.exponent,
                                                 self.save_svd, self.load_svd, self.svd_file)

        t2 = time.time()        # added by kwc
        print('%0.0f sec: jeo fit pre_factorization total' % (t2 - t1), file=sys.stderr)
        sys.stderr.flush()

        vectors = ProNE.chebyshev_gaussian(
            G.mat, features_matrix, self.n_components,
            step=self.step, mu=self.mu, theta=self.theta)

        t3 = time.time()        # added by kwc
        print('%0.0f sec: jeo fit chebyshev gaussian total' % (t3 - t2), file=sys.stderr)
        print('%0.0f sec: kwc ProNE chebyshev gaussian' % (t3 - t0), file=sys.stderr)
        sys.stderr.flush()

        self.model = dict(zip(G.nodes(), vectors))

    @staticmethod
    def tsvd_rand(matrix, n_components, save_svd, load_svd, svd_file):
        """
        Sparse randomized tSVD for fast embedding
        """
        print('jeo save_svd:', save_svd, file=sys.stderr)
        sys.stderr.flush()
        print('jeo load_svd:', load_svd, file=sys.stderr)
        sys.stderr.flush()
        print('jeo svd_file:', svd_file, file=sys.stderr)
        sys.stderr.flush()


        l = matrix.shape[0]
        # Is this csc conversion necessary?
        t0 = time.time()        # added by kwc
        smat = sparse.csc_matrix(matrix)
        t1 = time.time()        # added by kwc
        print('%0.0f sec: jeo tsvd_rand sparce csc matrix' % (t1 - t0), file=sys.stderr)
        sys.stderr.flush()
        print('Prone:', ProNE, file=sys.stderr)
        if load_svd:
            # added by jeo
            U = None
            try:
                print('jeo tsvd_rand_load - loading U matrix from: ', svd_file, file=sys.stderr)
                sys.stderr.flush()
                U = np.load(svd_file)
            except:
                # Keep preset values
                print('jeo error, tsvd_rand_load - loading U matrix from: ', svd_file, file=sys.stderr)
                sys.stderr.flush()
        else:
            t2 = time.time()        # added by kwc
            #import dask
            #dask.config.set({"optimization.fuse.ave-width": 5})
            import dask.array as da
            #da.config.set({"optimization.fuse.ave-width": 5})
            #U, Sigma, VT = randomized_svd(smat, 
            #    n_components=n_components, 
            #    n_iter=5, random_state=None)
            #U, Sigma, VT = da.linalg.svd_compressed(smat, k=10, compute=True)
            #U, Sigma, VT = da.linalg.svd_compressed(smat,n_power_iter=5, k=n_components, compute=True)
            print('jeo: shape smat before:', smat.shape, 'matrix details:', smat, 'matrix type: ', smat.getformat(), file=sys.stderr)
            #smat = smat[5000:]
            #smat = smat[1:5000, 1:5000]
            #smat = smat[0:5000, :]
            print('jeo: shape smat after:', smat.shape, 'matrix details:', smat, smat.getformat(), file=sys.stderr)
            x = da.from_array(smat, chunks=(100, 100))
            #x = da.from_array(smat, chunks=(1000, 1000))
            #x = da.from_array(smat, chunks=(100000, 100000))
            #U, Sigma, VT = da.linalg.svd_compressed(smat, k=n_components, compute=True)
            print('jeo tsvd: svd_compressed', file=sys.stderr)
            U, Sigma, VT = da.linalg.svd_compressed(x, k=n_components, compute=True)
            print('jeo tsvd: done', file=sys.stderr)
            #VT.compute()


            t3 = time.time()        # added by kwc
            print('%0.0f sec: jeo tsvd_rand randomized_svd' % (t3 - t2), file=sys.stderr)
            sys.stderr.flush()
            # added by kwc
            try:
                print('tsvd_rand: %d bytes for U (for %d n_components)' % (U.nbytes, n_components), file=sys.stderr)
                sys.stderr.flush()
            except:
                print('tsvd_rand: diagnostic msg failed', file=sys.stderr)
                sys.stderr.flush()
            U = U * np.sqrt(Sigma)
            U = preprocessing.normalize(U, "l2")
            if save_svd:
                try:
                    if not os.path.exists(svd_file):
                        os.makedirs(svd_file)
                        numpy_file = svd_file + "/" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3] + ".npy"
                        print('jeo tsvd_rand randomized_svd - saving U matrix to: ', svd_file, file=sys.stderr)
                        sys.stderr.flush()
                        np.save(numpy_file, U)
                except:
                    # Keep preset values
                    print('jeo error, tsvd_rand randomized_svd - saving U matrix to: ', svd_file, file=sys.stderr)
                    sys.stderr.flush()
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
        print('%0.0f sec: jeo chebyshev_gaussian svd_dense linalg.svd'  % (t1 - t0), file=sys.stderr)
        sys.stderr.flush()
        U = np.array(U)
        U = U[:, :dimension]
        s = s[:dimension]
        s = np.sqrt(s)
        U = U * s
        t2 = time.time()        # added by kwc
        U = preprocessing.normalize(U, "l2")
        t3 = time.time()        # added by kwc
        print('%0.0f sec: jeo chebyshev_gaussian svd_dense l2 normalize'  % (t3 - t2), file=sys.stderr)
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
        print('%0.0f sec: jeo chebyshev_gaussian LaPlacian conversion' % (t1 - t0), file=sys.stderr)
        
        # added by kwc
        try: 
            print('chebyshev_gaussian step 1 %0.0f sec: %f GB for Lx0 and %f for Lx1' % (time.time() - t0, Lx0.nbytes/1e9, Lx1.nbytes/1e9), file=sys.stderr)
        except:
            print('chebyshev_gaussian step 1 %0.0f sec: *** print failed ***' % (time.time()), file=sys.stderr)
            
        sys.stderr.flush()
        
        # Use Bessel function to get Chebyshev polynomials
        for i in range(2, step):
            t2 = time.time()        # added by kwc
            Lx2 = M.dot(Lx1)
            Lx2 = (M.dot(Lx2) - 2 * Lx1) - Lx0
            
            # added by kwc
            try:
                print('chebyshev_gaussian step %d %0.0f sec: %f GB for Lx0, %f GB for Lx1 and %f GB Lx2' % (i, time.time() - t0, Lx0.nbytes/1e9, Lx1.nbytes/1e9, Lx2.nbytes/1e9), file=sys.stderr)
            except:
                print('chebyshev_gaussian step %d %0.0f sec: *** print failed ***' % (i, time.time()), file=sys.stderr)
                
            if i % 2 == 0:
                conv += 2 * scipy.special.iv(i, theta) * Lx2
            else:
                conv -= 2 * scipy.special.iv(i, theta) * Lx2
            Lx0 = Lx1
            Lx1 = Lx2
            del Lx2
            t3 = time.time()        # added by kwc
            print('%0.0f sec: jeo chebyshev_gaussian Bessel for step' % (t3 - t2), file=sys.stderr)
            sys.stderr.flush()
        
        # added by kwc
        print('kwc chebyshev_gaussian finishing %0.0f sec' % (time.time() - t0), file=sys.stderr)
        
        mm = A.dot(a - conv)
        t4 = time.time()        # added by kwc
        emb = ProNE.svd_dense(mm, n_components)
        t5 = time.time()        # added by kwc
        print('%0.0f sec: jeo chebyshev_gaussian svd_dense' % (t5 - t4), file=sys.stderr)
        return emb
