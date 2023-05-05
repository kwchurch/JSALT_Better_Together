#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,argparse,urllib.parse
# from sklearn.metrics.pairwise import cosine_similarity

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
# parser.add_argument("--search", help="query", action='store_true')
parser.add_argument("--limit", type=int, help="max records to return", default=50)
args = parser.parse_args()

for line in sys.stdin:

    cmd = 'https://api.semanticscholar.org/graph/v1/paper/search?query=' + urllib.parse.quote_plus(line.rstrip()) + '&limit=' + str(args.limit)
    j = requests.get(cmd, headers={"x-api-key": apikey}).json()

    if 'data' in j:
        for r in j['data']:
            print(r['paperId'])
    else:
        print(j)
    sys.stdout.flush()



