#!/usr/bin/env python

# input: papers
# output: fanin (citations) and fanout (references) in citation graph

import numpy as np
import sys,json,requests,os,argparse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
parser.add_argument("--output_type", help="tsv|json [default]", default='json')
# parser.add_argument("--API", help="paper|author", default='paper')
# parser.add_argument("--search", help="query", action='store_true')
# parser.add_argument("--fields", help="comma separated fields", default='')
# parser.add_argument("--limit", type=int, help="max records to return", default=50)
args = parser.parse_args()

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def one_line_ify(s):
    return s.replace('\r', ' ').replace('\n', ' ')

def print_paper(paper, query):
    if args.output_type == 'json':
        print(paper)
        
    else:
        title = corpusid = None
        cites = 0
        if 'citationCount' in paper:
            cites = paper['citationCount']
        if 'externalIds' in paper and not paper['externalIds'] is None:
            corpusid = paper['externalIds']['CorpusId']
        if 'title' in paper:
            title = one_line_ify(paper['title'])
        print('\t'.join(map(str, [cites, query, corpusid, title])))
    
def citations(p):
    if 'citationCount' in p and not p['citationCount'] is None:
        return p['citationCount']
    else:
        return 0

def papers_by_citations(my_id):
    my_id = id_ify(query)
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=title,authors,referenceCount,citationCount,references,references.externalIds,references.citationCount,references.title,citations,citations.externalIds,citations.citationCount,citations.title'

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()

    if args.verbose:
        print(cmd)
        print(j)
    
    refs = []
    if 'references' in j and not j['references'] is None:
        refs = j['references']

    cites  = []
    if 'citations' in j and not j['citations'] is None:
        cites = j['citations']

    papers = refs
    papers.append(cites)

    return sorted(papers, reverse=True, key=citations)
    

for line in sys.stdin:
    query=line.rstrip()
    papers = papers_by_citations(query)

    for p in papers:
        print_paper(p, query)





