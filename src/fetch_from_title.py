#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,time,urllib,argparse

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--API", help="paper|author", default='paper')
parser.add_argument("--search", help="query", action='store_true')
parser.add_argument("--autocomplete", help="query", action='store_true')
parser.add_argument("--verbose", help="query", action='store_true')
args = parser.parse_args()

if args.search:
    url='https://api.semanticscholar.org/graph/v1/paper/search?fields=externalIds,title&query='
else:
    url='https://api.semanticscholar.org/graph/v1/paper/autocomplete?fields=externalIds,title&query='

if args.search:
    for line in sys.stdin:
        fields = line.rstrip().split('\t')
        suffix = '\t' + '\t'.join(fields)

        cmd=url + fields[0]
        j=requests.get(cmd, headers={"x-api-key": apikey}).json()
        if args.verbose: print(j)
        if not 'data' in j: j['data'] = []
        print('# %d matches:\t' % len(j['data']) + fields[0])
        for m in j['data']:
            print('\t'.join([str(m['externalIds']['CorpusId']), m['title']]) + suffix)
        sys.stdout.flush()
    
else:
    for line in sys.stdin:
        fields = line.rstrip().split('\t')
        suffix = '\t' + '\t'.join(fields)
        
        cmd=url + urllib.parse.quote(fields[0])
        j=requests.get(cmd, headers={"x-api-key": apikey}).json()

        if args.verbose:
            print(cmd, file=sys.stderr)
            print(j, file=sys.stderr)

        if not 'data' in j: j['data'] = []
        print('# %d matches:\t' % len(j['data']) + fields[0])
        for m in j['data']:
            print('\t'.join([str(m['externalIds']['CorpusId']), m['title']]) + suffix)
        sys.stdout.flush()

