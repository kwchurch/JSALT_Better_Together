#!/usr/bin/env python

import sys,json,os,gzip

def my_get(rec, keys):
    if len(keys) == 0:
        return rec
    elif isinstance(rec, dict) and keys[0] in rec:
        return my_get(rec[keys[0]], keys[1:])

def xyz2str(x):
    if x is None:
        return str(x)
    elif isinstance(x, str):
        return x
    elif isinstance(x, dict):
        return '|'.join(map(str, [ str(k) + ':' + str(v) for k,v in zip(x.keys(), x.values()) if not v is None ]))
    elif isinstance(x, list):
        return '|'.join(map(str, x))
    else:
        return str(x)

for f in sys.argv[1:]:
    with gzip.open(f) as fd:
        for line in fd:
            rline = line.rstrip()
            try:
                if len(rline) > 1:
                    j = json.loads(rline)
                    cid = my_get(j, ['corpusid'])
                    eids = xyz2str(my_get(j, ['externalids']))
                    pdfs = xyz2str(my_get(j, ['content', 'source', 'pdfurls']))
                    oa = xyz2str(my_get(j, ['content', 'source', 'oainfo', 'openaccessurl']))
                    print('\t'.join(map(str, [cid, eids, pdfs, oa])))
            except:
                print(rline, file=sys.stderr)

