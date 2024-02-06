#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,argparse,ast
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, help="max records to return", default=50)
args = parser.parse_args()

def id_ify(s):
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:', 'DBLP:', 'MAG:', 'PMID:']:
        if s.startswith(prefix):
            return s
    if '/' in s: return s
    return 'CorpusId:' + s

for line in sys.stdin:
    my_id = id_ify(line.rstrip())

    cmd = 'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/' + my_id + '/?from=all-cs&fields=externalIds,citationCount,year&limit=' + str(args.limit)
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()

    if 'recommendedPapers' in j:
        for rec in j['recommendedPapers']:
            if 'CorpusId' in rec['externalIds']:
                citations=year=-1
                if 'citationCount' in rec:
                    citations = rec['citationCount']
                if 'year' in rec:
                    year = rec['year']
                print('\t'.join(map(str, [line.rstrip(), rec['externalIds']['CorpusId'], year, citations])))
    sys.stdout.flush()





