#!/usr/bin/env python

# input: papers
# output: sentences from other papers that cite the paper in question

import numpy as np
import sys,json,requests,os,argparse

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

def one_line_ify(s):
    return s.replace('\r', ' ').replace('\n', ' ')

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], one_line_ify(paper['title'])])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

for line in sys.stdin:
    query=line.rstrip()
    my_id = id_ify(query)

    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=citations.externalIds'


    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if args.verbose:
        print(cmd)
        print(j)

    print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', one_line_ify(j['title'])])))

    if 'references' in j and not j['references'] is None:
        for reference in j['references']:
            print_paper(reference, 'reference', query)

    if 'citations' in j and not j['citations'] is None:
        for citation in j['citations']:
            print_paper(citation, 'citation', query)


