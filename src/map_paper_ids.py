#!/usr/bin/env python

import sys
import numpy as np

node_names_map = np.load(sys.argv[1])
direction = sys.argv[2]

assert direction in node_names_map, 'bad direction'

my_map = node_names_map[direction]

for line in sys.stdin:
    if len(line) > 1:
        paper = int(line.rstrip())
        if paper >= 0 and paper < len(my_map):
            print(str(paper) + '\t' + str(my_map[paper]))
        else:
            print(str(paper) + '\tNA')
