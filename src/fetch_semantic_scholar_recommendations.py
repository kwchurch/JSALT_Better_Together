#!/usr/bin/env python

# input: papers
# output: fanin (citations) and fanout (references) in citation graph

import numpy as np
import sys,json,requests,os,argparse
from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
# parser.add_argument("--API", help="paper|author", default='paper')
# parser.add_argument("--search", help="query", action='store_true')
# parser.add_argument("--fields", help="comma separated fields", default='')
parser.add_argument("--limit", type=int, help="max records to return", default=50)
args = parser.parse_args()

def old_id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:', 'DOI:', 'MAG:']:
        if s.startswith(prefix):
            return s

    fields = s.split('/')

    if s.startswith('https://doi.org/') and fields[-1].startswith('arXiv.'):
        p='arXiv:'
        return p + fields[-1][len(p):]

    p = '/doi/'
    pp = s.find(p)
    # print('pp = ' + str(pp), file=sys.stderr)
    if pp >= 0:
        pieces = s[pp + len(p):].split('/')
        return 'DOI:' + pieces[-2] + '/' + pieces[-1].split('?')[0]

    if s.startswith('https:'):
        for p,substr in [('DOI:', 'https://doi.org/'),
                         ('ACL:', 'https://aclanthology.org/'),
                         ('ACL:', 'https://www.aclweb.org/anthology/'),
                         ('PMID:', 'https://www.ncbi.nlm.nih.gov/pubmed/')]:
            if s.startswith(substr):
                return p + s[len(substr):]

    if s.startswith('https://www.semanticscholar.org/paper'):
        return fields[-1]


    if '/' in s: return s
    if '.' in s: return 'arXiv:' + s
    return 'CorpusId:' + s

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], paper['title']])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

def specter(cid):
    try:
        j = requests.get('https://api.semanticscholar.org/graph/v1/paper/' + str(cid) + '?fields=embedding', headers={"x-api-key": apikey}).json()
        return np.array(j['embedding']['vector'])
    except:
        return np.zeros(768) -1

for line in sys.stdin:
    query=line.rstrip()
    my_id = id_ify(query)
    qvec = specter(my_id).reshape(1,-1)


    cmd = 'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/' + my_id + '?fields=title,url,externalIds,citationCount&limit=' + str(args.limit)
    # cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=title,authors,referenceCount,citationCount,references,references.externalIds,references.citationCount,references.title,citations,citations.externalIds,citations.citationCount,citations.title'

    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    if args.verbose:
        print(cmd)
        print(j)

    # print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', j['title']]))) 

    for rec in j['recommendedPapers']:
        rec_vec = specter(rec['paperId']).reshape(1,-1)
        print('\t'.join(map(str, [query, rec['externalIds']['CorpusId'], cosine_similarity(qvec, rec_vec)[0,0], rec['citationCount'], rec['title']])))


