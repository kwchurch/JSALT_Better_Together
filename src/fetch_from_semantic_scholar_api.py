#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,argparse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--API", help="paper|author", default='paper')
parser.add_argument("--search", help="query", action='store_true')
parser.add_argument("--fields", help="comma separated fields", default='')
parser.add_argument("--limit", type=int, help="max records to return", default=50)
parser.add_argument("--debug", action='store_true')
parser.add_argument("--citations", action='store_true')
parser.add_argument("--recommendations", action='store_true')
parser.add_argument("--batch", action='store_true')
args = parser.parse_args()

def id_ify(s):
    if args.search or len(s) == 40 or args.API == 'author':
        return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:', 'DBLP:', 'MAG:', 'PMID:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

my_api = 'https://api.semanticscholar.org/graph/v1/' + args.API + '/'

if args.search:
    my_api = my_api + 'search?query='

batch_size=500

if args.batch:
    assert not args.recommendations, 'combination of --batch and --recommendations is not supported'
    lines = [ 'CorpusId:' + line for line in sys.stdin if len(line) > 1 ]
    ll = len(lines)
    batches = [lines[i:min(i+batch_size, ll)] for i in range(0, ll, batch_size)]
    for batch in batches:
        r = requests.post(
            'https://api.semanticscholar.org/graph/v1/paper/batch',
            params={'fields': 'externalIds,' + args.fields},
            json={"ids": batch},
            headers={"x-api-key": apikey}).json()
        # print(r)
        for rec in r:
            print(rec)
    sys.exit(0)

for line in sys.stdin:
    my_id = id_ify(line.rstrip())

    if args.citations:
        cmd = my_api + my_id + '/citations?fields=' + args.fields
    elif args.recommendations:
        cmd = 'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/' + my_id + '/?from=all-cs&fields=' + args.fields
    else:
        cmd = my_api + my_id + '/?fields=' + args.fields

    if args.API != 'author':
        cmd += '&limit=' + str(args.limit)

    # print(cmd)

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()

    if args.debug:
        print(j)

    if 'data' in j:
        for r in j['data']:
            print(r)
    elif 'papers' in j:
        for r in j['papers']:
            print(r)
    else:
        print(j)
    sys.stdout.flush()



