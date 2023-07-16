#!/usr/bin/env python

# import scipy
# from scipy import sparse, linalg, special
# from sklearn import preprocessing
import numpy as np
# from scipy.sparse import load_npz, csr_matrix, save_npz
import os,sys,argparse,time # ,gc,socket
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster import hierarchy # ,dendrogram
from matplotlib import pyplot as plt

# t0 = time.time()

# print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
# sys.stderr.flush()


parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, help="seed [defaults to 0 (non-deterministic)]", default=0)
parser.add_argument("-K", "--K", type=int, help="number of clusters", default=5)
parser.add_argument("--output_centroids", help="query", action='store_true')
parser.add_argument("--plot", help="query", action='store_true')
parser.add_argument("--output_labels", help="query", action='store_true')
parser.add_argument("--verbose", help="query", action='store_true')

# parser.add_argument("-o", "--output", help="output directory", required=True)
# parser.add_argument("-i", "--input", help="input npy prone file from ProNE_finish, or input npz file from ProNE baseline", required=True)
# parser.add_argument("-m", "--map", help="mapping files (from new_shrink_matrix)", required=True)
args = parser.parse_args()

if args.verbose:
    print('vec_to_kmeans.py: sys.argv = ' + str(sys.argv), file=sys.stderr)
    np.set_printoptions(precision=3, linewidth=200)

X = np.loadtxt(sys.stdin)
kmeans = KMeans(n_clusters=args.K, random_state=args.seed).fit(X[:,2:])
Z = hierarchy.complete(kmeans.cluster_centers_)
s = hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(Z, kmeans.cluster_centers_))

new_labels = s[kmeans.labels_]
new_centroids = kmeans.cluster_centers_[s,:]

sim = cosine_similarity(new_centroids)

if args.output_labels:
    np.savetxt(sys.stdout, new_labels, fmt='%d')

if args.output_centroids:
    np.savetxt(sys.stdout, new_centroids)

if args.verbose:
    print('s: ' + str(s), file=sys.stderr)
    labfreqs=np.bincount(s[kmeans.labels_])
    print('labfreqs: ' + str(labfreqs), file=sys.stderr)
    print(sim, file=sys.stderr)

if args.plot:
    plt.imshow(sim)
    plt.title("centroids")
    plt.colorbar()
    plt.show()

    sim2 = cosine_similarity(X[:,2:])
    sim3 = cosine_similarity(X[:,2:][np.argsort(kmeans.labels_),:])
    sim4 = cosine_similarity(X[:,2:][np.argsort(new_labels),:])

    plt.figure(figsize=(9,3))
    plt.subplot(131)
    plt.imshow(sim2)
    plt.title("unordered")

    plt.subplot(132)
    plt.imshow(sim3)
    plt.title("without optimal reordering")

    plt.subplot(133)
    plt.imshow(sim4)
    plt.title("with optimal reordering")

    plt.show()

