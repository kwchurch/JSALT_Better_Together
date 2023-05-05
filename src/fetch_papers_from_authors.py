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

for line in sys.stdin:
    author=line.rstrip()

    cmd = 'https://api.semanticscholar.org/graph/v1/author/' + author + '/?fields=name,papers,papers.citationCount,papers.externalIds,papers.title,hIndex,citationCount,externalIds,url,name,affiliations,papers.authors'

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if args.verbose:
        print(cmd)
        print(j)

    try:
        candidates = sorted([ (p['externalIds']['CorpusId'], p['citationCount'], p['title'], p['authors']) for p in j['papers'] if 'externalIds' in p], key= lambda pair: pair[1], reverse=True)
        print('\t'.join(map(str,['AuthorInfo', author, j['hIndex'], j['citationCount'], len(candidates), j['externalIds'], j['url'], j['name'], j['affiliations']])))
        for paper,citations,title,authors in candidates:
            print('\t'.join(map(str, [author, j['name'], paper, citations, safe(title), authors])))
    except:
        print('***ERROR***\tauthor: ' + author + '\t' + str(j))

    # print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', j['title']])))

    # if 'references' in j and not j['references'] is None:
    #     for reference in j['references']:
    #         print_paper(reference, 'reference', query)

    # if 'citations' in j and not j['citations'] is None:
    #     for citation in j['citations']:
    #         print_paper(citation, 'citation', query)


