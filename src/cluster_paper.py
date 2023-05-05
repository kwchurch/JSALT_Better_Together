#!/usr/bin/env python

import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
# from sklearn.cluster import AgglomerativeClustering
# from matplotlib import pyplot as plt


X = np.loadtxt(sys.stdin)
np.set_printoptions(precision=2,linewidth=200)
scores = cosine_similarity(X[:,2:])

# model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)
# model = model.fit(x[:,2:])
# s = model.labels_
# np.savetxt(sys.stdout, x[:,0][s], fmt='%d')

import numpy as np
# from scipy.cluster import hierarchy # ,dendrogram
# Z = hierarchy.ward(x)
# s = hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(Z, x))

# scores = cosine_similarity(x[:,2:])[s,:][:,s]
np.set_printoptions(precision=2,linewidth=200, edgeitems=15, suppress=True)
print('scores: %0.4f +- %0.3f, shape: %s' % (np.mean(scores), np.sqrt(np.var(scores)), str(scores.shape)), file=sys.stderr)
print('quantiles: ' + str(np.quantile(scores, np.linspace(0,1,20))), file=sys.stderr)
print(scores, file=sys.stderr)

# # dendrogram(Z)

# np.savetxt(sys.stdout, x[:,0][s], fmt='%d')

from sklearn.cluster import KMeans
Y = X[0,2:].reshape(1,-1)
kmeans = KMeans(n_clusters=np.int32(np.round(np.sqrt(X.shape[0])))).fit(X[:,2:][1:,:])
scores2 = cosine_similarity(kmeans.cluster_centers_)
scores3 = cosine_similarity(Y, kmeans.cluster_centers_)[0,:]
labfreqs=np.bincount(kmeans.labels_)

print('scores2: %0.4f +- %0.3f, shape: %s' % (np.mean(scores2), np.sqrt(np.var(scores2)), str(scores2.shape)), file=sys.stderr)
print('quantiles2: ' + str(np.quantile(scores2, np.linspace(0,1,20))), file=sys.stderr)
print('bincount: ' + str(labfreqs), file=sys.stderr)
print('scores from query to centroids: ' + str(scores3), file=sys.stderr)
print(scores2, file=sys.stderr)

for i in range(len(kmeans.labels_)):
    lab = kmeans.labels_[i]
    id = X[1+i,0]
    print('%d\t%0.3f\t%0.3f\t%d\t%d\t%d' % (lab, cosine_similarity(Y, X[1+i,2:].reshape(1,-1))[0,0], scores3[lab], labfreqs[lab], id, id))


