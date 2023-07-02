#!/usr/bin/env python

import sys,json,gzip,os,argparse

parser = argparse.ArgumentParser()
# default='/mnt/big/kwc/morphology/embedding_comparisons/annoys.txt'
parser.add_argument("-i", "--input", help="a filename", default='authors.piece.%03d.gz')
parser.add_argument("-o", "--output", help="output file", default='authors.piece.%03d.id')
# parser.add_argument("-H", "--hindex", type=int, help="threshold on hindex", default=0)
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
    
print('hindex\tpapercount\tcitationcount\tauthorid\tname', file=out_fd)

with gzip.open(inf) as in_fd:
    for line in in_fd:
        rline = line.rstrip()
        j = json.loads(rline)
        hindex = authorid  = name = papercount = citationcount = 'NA'
        if 'hindex' in j: hindex = j['hindex']
        if 'authorid' in j: authorid = j['authorid']
        if 'name' in j: name = j['name']
        if 'papercount' in j: papercount  = j['papercount']
        if 'citationcount' in j: citationcount = j['citationcount']
        
        print('\t'.join(map(str, [hindex, papercount, citationcount, authorid, name])), file=out_fd)

