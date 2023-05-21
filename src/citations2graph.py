#!/usr/bin/env python

import sys,json,gzip

errors=0
for f in sys.argv[1:]:
    X_fd = open(f + '.X.txt', 'w')
    Y_fd = open(f + '.Y.txt', 'w')
    with gzip.open(f) as fd:
        for line in fd:
            rline = line.rstrip()
            if len(rline) > 1:
                try:
                    j = json.loads(rline)
                    id1 = j["citingcorpusid"]
                    id2 = j["citedcorpusid"]
                    if not id1 is None and not id2 is None:
                        print(str(id1), file=X_fd)
                        print(str(id2), file=Y_fd)
                except:
                    errors += 1
                    print(rline, file=sys.stderr)

print('%0d errors' % errors, file=sys.stderr)
