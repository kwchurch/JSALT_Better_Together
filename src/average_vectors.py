#!/usr/bin/env python

import numpy as np
import sys
from sklearn.preprocessing import normalize

x = np.loadtxt(sys.stdin)
# print(np.linalg.norm(x, axis=0), file=sys.stderr)
x = normalize(x)
# print(np.linalg.norm(x, axis=0), file=sys.stderr)
x = np.mean(x, axis=0)
# print(np.linalg.norm(x), file=sys.stderr)
x /= np.linalg.norm(x)
# print(np.linalg.norm(x), file=sys.stderr)
np.savetxt(sys.stdout, x)

