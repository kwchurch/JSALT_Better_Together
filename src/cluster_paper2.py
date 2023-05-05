#!/usr/bin/env python

import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.stats import trim_mean
# from sklearn.cluster import AgglomerativeClustering
# from matplotlib import pyplot as plt


rawX = np.loadtxt(sys.stdin)
X = rawX[:,2:]
Y= X[0,:].reshape(1, -1)
X = X[1:,:]

centroid = np.mean(X, axis=0).reshape(1, -1)
trim1_centroid = trim_mean(X, 0.05, axis=0).reshape(1, -1)
trim2_centroid = trim_mean(X, 0.10, axis=0).reshape(1, -1)

# print(centroid.shape)

np.set_printoptions(precision=2,linewidth=200)
# scores = cosine_similarity(X[:,2:])
# model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
# model = model.fit(x[:,2:])
# s = model.labels_
# np.savetxt(sys.stdout, x[:,0][s], fmt='%d')

# from scipy.cluster import hierarchy # ,dendrogram
# Z = hierarchy.ward(x)
# s = hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(Z, x))

# scores = cosine_similarity(x[:,2:])[s,:][:,s]
# np.set_printoptions(precision=2,linewidth=200, edgeitems=15, suppress=True)
# print('scores: %0.4f +- %0.3f, shape: %s' % (np.mean(scores), np.sqrt(np.var(scores)), str(scores.shape)), file=sys.stderr)
# print('quantiles: ' + str(np.quantile(scores, np.linspace(0,1,20))), file=sys.stderr)
# print(scores, file=sys.stderr)

# # # dendrogram(Z)

# # np.savetxt(sys.stdout, x[:,0][s], fmt='%d')

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=np.int32(np.round(np.sqrt(X.shape[0])))).fit(X)
# kmeans = KMeans(n_clusters=X.shape[0]//3).fit(X)
labfreqs=np.bincount(kmeans.labels_)
labfreqsidx = np.argsort(-labfreqs)
# print(labfreqs)
# print(labfreqsidx)

T=3
idx = labfreqsidx
if len(labfreqs) > T:
    idx = labfreqsidx[0:T]

# print('query: ' + str(np.int64(rawX[0,0])))
# print('centroid: ' + str(cosine_similarity(centroid, Y)[0,0]))
# print(scores)
# print(labfreqs[idx])

query = np.int64(rawX[0,0])

def str_ify(x):
    return '\t'.join(map(str, x))

print(str_ify([query,
               '%0.3f' % cosine_similarity(centroid, Y)[0,0], 
               '%0.3f' % cosine_similarity(trim1_centroid, Y)[0,0], 
               '%0.3f' % cosine_similarity(trim2_centroid, Y)[0,0], 
               X.shape[0],
               # str_ify(cosine_similarity(kmeans.cluster_centers_[idx,:], Y).reshape(-1)),
               str_ify([ '%0.3f' % cosine_similarity(kmeans.cluster_centers_[i,:].reshape(1,-1), Y)[0,0] for i in idx ]),
               str_ify(labfreqs[idx])]))

# print('\t'.join(map(str, [np.int64(rawX[0,0]),
#                           cosine_similarity(best_centroid, Y), labfreqs[labfreqsidx[-1]],
#                           cosine_similarity(runnerup_centroid, Y), labfreqs[labfreqsidx[-2]],
#                           cosine_similarity(second_runnerup_centroid, Y), labfreqs[labfreqsidx[-3]],
#                           cosine_similarity(centroid, Y)[0,0]
#                       ])))

# scores2 = cosine_similarity(kmeans.cluster_centers_)
# scores3 = cosine_similarity(X[0,2:].reshape(1,-1), kmeans.cluster_centers_)[0,:]
# 

# print('scores2: %0.4f +- %0.3f, shape: %s' % (np.mean(scores2), np.sqrt(np.var(scores2)), str(scores2.shape)), file=sys.stderr)
# print('quantiles2: ' + str(np.quantile(scores2, np.linspace(0,1,20))), file=sys.stderr)
# print('bincount: ' + str(labfreqs), file=sys.stderr)
# print('scores from query to centroids: ' + str(scores3), file=sys.stderr)
# print(scores2, file=sys.stderr)

# for id,lab in zip(X[1:,0], kmeans.labels_):
#     print('%d\t%0.3f\t%d\t%d\t%d' % (lab, scores3[lab], labfreqs[lab], id, id))


