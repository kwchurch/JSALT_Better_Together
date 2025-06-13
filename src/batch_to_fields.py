#!/usr/bin/env python

import requests,sys,json,os,time

apikey=os.environ.get('SPECTER_API_KEY')
# fields='externalIds,title,abstract,embedding.specter_v2'
if len(sys.argv) < 2:
    fields='externalIds,title,abstract,embedding.specter_v2'
else:
    fields=sys.argv[1]

lines = ["CorpusId:" + line.rstrip() for line in sys.stdin]
batch_size = 500
ll = len(lines)
batches = [lines[i:min(i+batch_size, ll)] for i in range(0, ll, batch_size)]

def do_it(ids, tries):
    r = None
    for i in range(tries):
        r = requests.post(
            'https://api.semanticscholar.org/graph/v1/paper/batch',
            params={'fields': fields},
            json={"ids": ids },
            headers={"x-api-key": apikey}).json()
        if isinstance(r, list):
            return r
        time.sleep(30)
    return r
    
for ids in batches:
    r = do_it(ids, 20)
    if isinstance(r, list):
        for r1 in r:
            print(r1)
    else:
        print(r)
    time.sleep(10)



