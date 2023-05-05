#!/usr/bin/env python

import sys,os,time,argparse
import numpy as np


t0 = time.time()

slurm=os.environ.get('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(os.environ.get('SLURM_ARRAY_TASK_ID')), file=sys.stderr)
sys.stderr.flush()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
parser.add_argument("-H", "--header", default=None)
parser.add_argument("-s", "--suffix", default='')
parser.add_argument("-t", "--type", default='uint8')
args = parser.parse_args()

if slurm is None:
    infile = args.input
else:
    slurm = '%03d' % int(slurm)
    infile = args.input + '.' + slurm + args.suffix


# parser = argparse.ArgumentParser()
# parser.add_argument("-i", "--input", required=True)
# parser.add_argument("-o", "--output", required=True)
# parser.add_argument("-N", "--N", type=int, default=None)
# args = parser.parse_args()

if args.type == 'uint8':
    dtype=np.uint8
    zeros = np.zeros(256, dtype=int)
elif args.type == 'uint16':
    dtype=np.uint16
    zeros = np.zeros(65536, dtype=int)
else: assert False, 'bad -t arg: ' + args.type

X = np.fromfile(infile, dtype=dtype)
C = np.bincount(X)
zeros[0:len(C)]=C
C=zeros

with open(args.output, 'w') as fd:
    if not args.header is None:
        print(args.header, file=fd)
    np.savetxt(fd, C, fmt='%d')

print(str(time.time() - t0) + ' done', file=sys.stderr)
sys.stderr.flush()
