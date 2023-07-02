#!/usr/bin/env python

import sys,json,gzip,os

errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

if slurm is None:
    inf = sys.argv[1]
    outf = sys.stdout
else:
    inf = '/work/k.church/semantic_scholar/papers/papers.piece.%03d.gz' % int(slurm)
    outf = open('/work/k.church/semantic_scholar/papers/papers2url/papers.piece.%03d.id' % int(slurm), 'w')
    print('inf: ' + str(inf), file=sys.stderr)

with gzip.open(inf) as fd:
    for line in fd:
        rline = line.rstrip()
        if len(rline) > 1:
            try:
                j = json.loads(rline)
                id = j['corpusid']
                url = j['url']
                urlhex = url.split('/')[-1]
                print(str(id) + '\t' + str(urlhex), file=outf)
            except:
                errors += 1
                print('error %d: %s' %(errors, rline), file=sys.stderr)

print('%0d errors' % errors, file=sys.stderr)
