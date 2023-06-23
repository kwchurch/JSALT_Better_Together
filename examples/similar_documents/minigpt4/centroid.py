import numpy as np
import sys

x = np.loadtxt(sys.stdin)
centroid = np.sum(x[:,2:], axis=0)
print(centroid.shape)

