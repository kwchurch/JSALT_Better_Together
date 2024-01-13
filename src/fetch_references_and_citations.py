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
parser.add_argument("--limit", type=int, help="max records to return", default=1000)
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
        year = 'NA'
        if 'year' in paper:
            year = str(paper['year'])
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], year, one_line_ify(paper['title'])])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

def do_references(query, my_id):
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=referenceCount,citationCount,title'
    jj = requests.get(cmd, headers={"x-api-key": apikey}).json()
    refs = 0
    if 'referenceCount' in jj:
        refs = jj['referenceCount']

    if refs > args.limit:
        refs = args.limit

    for offset in range(0,refs+1000,1000):
        # cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=references,references.externalIds,references.citationCount,references.title&limit=1000&offset=' + str(offset)
        cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/references?fields=externalIds,citationCount,title&limit=1000&offset=' + str(offset)
        j = requests.get(cmd, headers={"x-api-key": apikey}).json()
        if args.verbose:
            print(cmd)
            print(j)
            print('\t'.join(map(str,['query', str(jj['referenceCount']) + ' references', str(jj['citationCount']) + ' citations', one_line_ify(jj['title'])])))
        
        if 'data' in j and not j['data'] is None:
            for reference in j['data']:
                for p in reference.values():
                    print_paper(p, 'reference', query)


def do_citations(query, my_id):
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=referenceCount,citationCount,title'
    jj = requests.get(cmd, headers={"x-api-key": apikey}).json()
    cites = 0
    if 'citationCount' in jj:
        cites = jj['citationCount']

    if cites > args.limit:
        cites = args.limit

    for offset in range(0,cites+1000,1000):
        # cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=references,references.externalIds,references.citationCount,references.title&limit=1000&offset=' + str(offset)
        # cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=citations,citations.externalIds,citations.citationCount,citations.title,citations.year&limit=1000&offset=' + str(offset)
        cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/citations?fields=externalIds,citationCount,title,year&limit=1000&offset=' + str(offset)
        j = requests.get(cmd, headers={"x-api-key": apikey}).json()
        if args.verbose:
            print(cmd)
            print(j)
            print('\t'.join(map(str,['query', str(jj['referenceCount']) + ' references', str(jj['citationCount']) + ' citations', one_line_ify(jj['title'])])))
        
        if 'data' in j and not j['data'] is None:
            for citation in j['data']:
                print_paper(citation['citingPaper'], 'citation', query)


def do_it(query, my_id):

    do_references(query, my_id)
    do_citations(query, my_id)
            
    # offset=0
    # while(True):

    #     done=1

    #     cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=title,authors,referenceCount,citationCount,references,references.externalIds,references.citationCount,references.title,citations,citations.externalIds,citations.citationCount,citations.title,citations.year&limit=1000&offset=' + str(offset)

    #     offset += 1000

    #     j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    #     if args.verbose:
    #         print(cmd)
    #         print(j)
    #         print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', one_line_ify(j['title'])])))

    #     if 'references' in j and not j['references'] is None:
    #         for reference in j['references']:
    #             print_paper(reference, 'reference', query)
    #             done=0

    #     if 'citations' in j and not j['citations'] is None:
    #         for citation in j['citations']:
    #             print_paper(citation, 'citation', query)
    #             done=0

    #     if done>0: return

    

if args.limit <= 1000:
    for line in sys.stdin:
        query=line.rstrip()
        my_id = id_ify(query)
        
        cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/?fields=title,authors,referenceCount,citationCount,references,references.externalIds,references.citationCount,references.title,citations,citations.externalIds,citations.citationCount,citations.title,citations.year&limit=' + str(args.limit)


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

else:
    for line in sys.stdin:
        query=line.rstrip()
        my_id = id_ify(query)
        do_it(query, my_id)

        
                


