#!/usr/bin/env python

import sys,scipy.sparse,time,argparse,os,socket
import numpy as np
import random

t0 = time.time()

print(str(time.time() - t0) + ' host: %s, SLURM_JOB_ID: %s, SLURM_ARRAY_TASK_ID: %s' % (socket.gethostname(), os.environ.get('SLURM_JOB_ID'), os.environ.get('SLURM_ARRAY_TASK_ID'), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-G", "--graph", help=".npz file", required=True)
parser.add_argument("-X", "--axis", type=int, help="arg to np.sum", required=True)
parser.add_argument("-o", "--output", help="output", required=True)
parser.add_argument("-T", '--transpose', action='store_true')
args = parser.parse_args()

def my_load(f):
    print(str(time.time() - t0) + ' my_load: ' + f, file=sys.stderr)
    sys.stderr.flush()
    return scipy.sparse.load_npz(f)

M = my_load(args.graph)
print(str(time.time() - t0) + ' finished loading', file=sys.stderr)
sys.stderr.flush()

if args.transpose:
    M = M.T

print(str(time.time() - t0) + ' finished transposing: args.transpose = ' + str(args.transpose), file=sys.stderr)

S = np.sum(M, axis=args.axis)

print(str(time.time() - t0) + ' finished summing', file=sys.stderr)
sys.stderr.flush()

np.save(args.output, S)

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
