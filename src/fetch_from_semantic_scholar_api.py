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
args = parser.parse_args()

def id_ify(s):
    if args.search or len(s) == 40 or args.API == 'author':
        return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

my_api = 'https://api.semanticscholar.org/graph/v1/' + args.API + '/'

if args.search:
    my_api = my_api + 'search?query='

for line in sys.stdin:
    my_id = id_ify(line.rstrip())

    if args.citations:
        cmd = my_api + my_id + '/citations?fields=' + args.fields
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



