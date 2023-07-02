#!/usr/bin/env python

import sys,json,gzip,os,argparse

parser = argparse.ArgumentParser()
# default='/mnt/big/kwc/morphology/embedding_comparisons/annoys.txt'
parser.add_argument("-i", "--input", help="a filename", default='authors.piece.%03d.gz')
parser.add_argument("-o", "--output", help="output file", default='authors.piece.%03d.id')
parser.add_argument("-H", "--hindex", type=int, help="threshold on hindex", default=0)
args = parser.parse_args()

errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

if slurm is None:
    inf = args.input
    outf = args.output
else:
    inf = args.input % int(slurm)
    outf = args.output % int(slurm)

if outf == '-':
    out_fd = sys.stdout
else:
    out_fd = open(outf, 'w')
    
with gzip.open(inf) as in_fd:
    for line in in_fd:
        rline = line.rstrip()
        j = json.loads(rline)
        if 'hindex' in j and int(j['hindex']) >= args.hindex:
            print(j['authorid'], file=out_fd)

