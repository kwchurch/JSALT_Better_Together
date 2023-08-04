#!/usr/bin/env python

# input: authors
# output: papers 

import numpy as np
import sys,json,requests,os,argparse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
args = parser.parse_args()

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], paper['title']])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

def safe(s):
    return s.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

def do_authorid(authorid):
    print('do_authorid: ' + str(authorid), file=sys.stderr)
    cmd = 'https://api.semanticscholar.org/graph/v1/author/' + str(authorid) + '/?fields=name,papers,papers.citationCount,papers.externalIds,papers.title,hIndex,citationCount,externalIds,url,name,affiliations,papers.authors'

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if args.verbose:
        print(cmd)
        print(j)

    try:
        candidates = sorted([ (p['externalIds']['CorpusId'], p['citationCount'], p['title'], p['authors']) for p in j['papers'] if 'externalIds' in p], key= lambda pair: pair[1], reverse=True)
        print('\t'.join(map(str,['AuthorInfo', authorid, j['hIndex'], j['citationCount'], len(candidates), j['externalIds'], j['url'], j['name'], j['affiliations']])))
        for paper,citations,title,authors in candidates:
            print('\t'.join(map(str, [authorid, j['name'], paper, citations, safe(title), authors])))
    except:
        print('***ERROR***\tauthor: ' + authorid + '\t' + str(j))

for line in sys.stdin:
    author=line.rstrip()
    # print('author: ' + str(author), file=sys.stderr)
    if len(author) == 0: continue
    
    try:
        do_authorid(int(author))
    except:
        # print('author (after exception): ' + str(author), file=sys.stderr)
        # fields = '&fields=hindex,papers
        fields = '&fields=name,papers,papers.citationCount,papers.externalIds,papers.title,hIndex,citationCount,externalIds,url,name,affiliations,papers.authors'
        j = requests.get('https://api.semanticscholar.org/graph/v1/author/search?query=' + author + fields, headers={"x-api-key": apikey}).json()
        # print('j: ' + str(j))

        for rec in j['data']:
            if not 'hIndex' in rec or rec['hIndex'] is None:
                rec['hIndex'] = 0

        for rec in sorted(j['data'],
                          reverse=True,
                          key=lambda x: x['hIndex']):
            candidates = sorted([ (rec['authorId'], rec['hIndex'], rec['name'],
                                   p['externalIds']['CorpusId'], p['citationCount'], safe(p['title']),
                                   '|'.join([a['name'] for a in p['authors']]))
                                  for p in rec['papers'] if 'externalIds' in p], 
                                key= lambda pair: pair[4], reverse=True)
            for rec in candidates:
                print('\t'.join(map(str,rec)))
                # do_authorid(rec['authorId'])
        



