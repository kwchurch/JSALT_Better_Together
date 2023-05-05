#!/usr/bin/env python

# input: papers
# output: fanin (citations) and fanout (references) in citation graph

import numpy as np
import sys,json,requests,os,argparse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
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

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], paper['title']])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

for line in sys.stdin:
    query=line.rstrip()
    my_id = id_ify(query)

    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=title,authors,referenceCount,citationCount,references,references.externalIds,references.citationCount,references.title,citations,citations.externalIds,citations.citationCount,citations.title'


    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if args.verbose:
        print(cmd)
        print(j)

    print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', j['title']])))

    if 'references' in j and not j['references'] is None:
        for reference in j['references']:
            print_paper(reference, 'reference', query)

    if 'citations' in j and not j['citations'] is None:
        for citation in j['citations']:
            print_paper(citation, 'citation', query)


