#!/usr/bin/env python

import sys,json,gzip,os

errors=0

with gzip.open(sys.argv[1]) as fd:
    for line in fd:
        rline = line.rstrip()
        if len(rline) > 1:
            try:
                j = json.loads(rline)
                print(j['corpusid'])
            except:
                errors += 1

print('%0d errors' % errors, file=sys.stderr)
