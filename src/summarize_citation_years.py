#!/usr/bin/env python

import sys
import numpy as np

years = np.load(sys.argv[1])

N = max(np.max(years['Xyears']), np.max(years['Yyears'])) + 1

res = np.zeros((N, N), dtype=int)
# np.save(sys.argv[2], res)

for x,y in zip(years['Xyears'], years['Yyears']):
    res[x,y] += 1

np.save(sys.argv[2], res)
