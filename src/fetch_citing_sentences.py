#!/usr/bin/env python

# input: papers
# output: sentences from other papers that cite the paper in question

import numpy as np
import sys,json,requests,os,argparse

apikey=os.environ.get('SPECTER_API_KEY')

if apikey is None:
    print('Warning: it is highly recommended that you get an api key from Semantic Scholar, and set it to the environment variable, SPECTER_API_KEY', file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="query", action='store_true')
parser.add_argument("--offset", type=int,  help="start of papers to return (defaults to 0)", default=0)
parser.add_argument("--limit", type=int,  help="number of papers to return (max is 1000)", default=100)
parser.add_argument("--output_format", help="json|text", default="text")
parser.add_argument("--output", help="output file name (required for Windows)", default=None)
args = parser.parse_args()

if args.output is None:
    outf = sys.stdout
else:
    outf = open(args.output, 'w', encoding="UTF-8")

def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

def one_line_ify(s):
    return str(s).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')

def print_paper(paper, link_type, query):
    # print(paper)
    if 'externalIds' in paper and not paper['externalIds'] is None:
        print('\t'.join(map(str, [link_type, query, paper['externalIds']['CorpusId'], paper['citationCount'], one_line_ify(paper['title'])])))
    else:
        print('\t'.join(map(str, [link_type, query, '*** ERROR ***', paper])))

def do_it(my_id, low, hi):
    print('do_it: my_id = %s, low = %s, hi  = %s' % (str(my_id), str(low), str(hi)), file=sys.stderr)
    if low >= hi: return
    cmd = 'https://api.semanticscholar.org/graph/v1/paper/' + my_id + '/citations?fields=contexts,referenceCount,citationCount,title,externalIds,year'
    cmd = cmd + '&offset=' + str(low)
    cmd = cmd + '&limit=' + str(hi-low)

    # if not args.offset is None:
    #     cmd = cmd + '&offset=' + str(args.offset)

    # if not args.limit is None:
    #     cmd = cmd + '&limit=' + str(args.limit)

    if not apikey is None:
        j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    else:
        j = requests.get(cmd).json()
    if args.verbose:
        print(cmd)
        print(j)

    if args.output_format == 'json':
        print(json.dumps(j), file=outf)
    elif 'data' in j:
        if not 'data' in j:
            print('*** ERROR (no data) ***: ' + json.dumps(j), file=outf)
        else:
            for rec in j['data']:
                if 'citingPaper' in rec:
                    p = rec['citingPaper']
                    if p is None: continue
                    try:
                        print('\t'.join(map(one_line_ify, [p['externalIds']['CorpusId'],
                                                           p['year'], 
                                                           p['citationCount'], 
                                                           p['referenceCount'], 
                                                           p['title'], 
                                                           rec['contexts']])),
                              file=outf)
                    except:
                        print('*** ERROR ***: ' + json.dumps(j), file=outf)


for line in sys.stdin:
    query=line.rstrip()
    my_id = id_ify(query)

    cites = 0
    cmd='http://recommendpapers.xyz:8080/api/lookup_paper?id=' + my_id + '&fields=title,citationCount'
    print('cmd=' + str(cmd), file=sys.stderr)
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()
    print('j=' + str(j), file=sys.stderr)
    if 'papers' in j:
        for p in j['papers']:
            if 'citationCount' in p:
                cites = p['citationCount']
                print('cites=' + str(cites), file=sys.stderr)

                step=1000
                if cites > 0:
                    for i in range(0, cites, step):
                        do_it(my_id, i, min(i+step, cites))
    

    # # print('\t'.join(map(str,['query', str(j['referenceCount']) + ' references', str(j['citationCount']) + ' citations', one_line_ify(j['title'])])))

    # if 'references' in j and not j['references'] is None:
    #     for reference in j['references']:
    #         print_paper(reference, 'reference', query)

    # if 'citations' in j and not j['citations'] is None:
    #     for citation in j['citations']:
    #         print_paper(citation, 'citation', query)


