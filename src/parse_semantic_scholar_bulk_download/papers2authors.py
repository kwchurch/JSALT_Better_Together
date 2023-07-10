#!/usr/bin/env python

import sys,json,gzip,os,hashlib

errors=0

slurm=os.getenv('SLURM_ARRAY_TASK_ID')

print('SLURM_ARRAY_TASK_ID: ' + str(slurm), file=sys.stderr)

def h(obj):
    return hashlib.md5(str(obj).encode('utf-8')).hexdigest()

def clean(s):
    return s.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

if slurm is None:
    inf = sys.argv[1]
    outf = sys.stdout
else:
    inf = sys.argv[1] % int(slurm)
    outf = open(sys.argv[2] % int(slurm), 'w')
    print('inf: ' + str(inf), file=sys.stderr)

with gzip.open(inf) as fd:
    for line in fd:
        rline = line.rstrip()
        if len(rline) > 1:
            try:
                j = json.loads(rline)
                id = str(j['corpusid'])
                for rec in j['authors']:
                    print(id + '\t' + str(rec['authorId']), file=outf)
            except:
                errors += 1

print('%0d errors' % errors, file=sys.stderr)
