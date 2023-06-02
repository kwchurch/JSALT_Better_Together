#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,argparse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
# parser.add_argument("--API", help="paper|author", default='paper')
# parser.add_argument("--search", help="query", action='store_true')
# parser.add_argument("--fields", help="comma separated fields", default='')
# parser.add_argument("--limit", type=int, help="max records to return", default=50)
parser.add_argument("--debug", action='store_true')
# parser.add_argument("--citations", action='store_true')
args = parser.parse_args()

memos = {}

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:', 'DBLP:', 'MAG:', 'PMID:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

my_api = 'https://api.semanticscholar.org/graph/v1/paper/'

# if args.search:
#     my_api = my_api + 'search?query='

def clean(s):
    return s.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

def snippet(r):
    if args.debug: print('r: ' + str(r), file=sys.stderr)
    if 'error' in r:
        return r['error']
    if not 'paperId' in r:
        print('expected paperId in: ' + str(r), file=sys.stderr)
        return 'NA'
    paper = r['paperId']
    citations = r['citationCount']
    title = clean(r['title'])
    return '<a href="https://www.semanticscholar.org/paper/%s">%d: %s</a>' % (paper, citations, title)

def snippet_field(field):
    my_id = id_ify(field)
    if not my_id in memos:
        cmd = my_api + my_id + '/?fields=title,citationCount'
        j = requests.get(cmd, headers={"x-api-key": apikey}).json()

        if args.debug: print(j, file=sys.stderr)
        
        if 'data' in j:
            memos[my_id] = '|'.join([snippet(r) for r in j['data']])
        elif 'papers' in j:
            memos[my_id] = '|'.join([snippet(r) for r in j['papers']])
        else: memos[my_id] = snippet(j)
    return memos[my_id]

for line in sys.stdin:
    print('\t'.join([snippet_field(field) for field in line.rstrip().split('\t')]))




