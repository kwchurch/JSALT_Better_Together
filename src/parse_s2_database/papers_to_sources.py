#!/usr/bin/env python

import sys,json,os,gzip

errors=0

def my_get(rec, keys):
    if len(keys) == 0:
        return rec
    elif isinstance(rec, dict) and keys[0] in rec:
        return my_get(rec[keys[0]], keys[1:])

for f in sys.argv[1:]:
    with gzip.open(f) as fd:
        for line in fd:
            rline = line.rstrip()
            if len(rline) > 1:
                j = json.loads(rline)
                cid = my_get(j, ['corpusid'])
                ids = my_get(j, ['externalids'])
                if ids is None: continue
                sources = [ k for k in ids if not ids[k] is None ]
                print(str(cid) + '\t' + '\t'.join(map(str, sources)))

print(str(errors) + ' errors', file=sys.stderr)



