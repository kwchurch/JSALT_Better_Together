#!/usr/bin/env python

import sys,json,gzip,os

errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

if slurm is None:
    inf = sys.argv[1]
    outf = sys.stdout
else:
    inf = 'authors.piece.%03d.gz' % int(slurm)
    outf = open('authors.piece.%03d.url' % int(slurm), 'w')
    print('inf: ' + str(inf), file=sys.stderr)

with gzip.open(inf) as fd:
    for line in fd:
        rline = line.rstrip()
        try:
            j = json.loads(rline)
            print('<a href="%s">%s</a>' % (j['url'], j['name']), file=outf)
        except:
            errors += 1

print('done: %d errors' % errors, file=sys.stderr)

