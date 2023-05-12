#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,time,urllib,argparse

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("--API", help="paper|author", default='paper')
parser.add_argument("--search", help="query", action='store_true')
parser.add_argument("--autocomplete", help="query", action='store_true')
args = parser.parse_args()

if args.search:
    url='https://api.semanticscholar.org/graph/v1/paper/search?query='
else:
    url='https://api.semanticscholar.org/graph/v1/paper/autocomplete?query='

if args.autocomplete:
    for line in sys.stdin:
        fields = line.rstrip().split('\t')
        suffix = '\t' + '\t'.join(fields)
        
        cmd=url + urllib.parse.quote(fields[0])
        j=requests.get(cmd, headers={"x-api-key": apikey}).json()
        print('# %d matches:\t' % len(j['matches']) + fields[0])
        for m in j['matches']:
            print('\t'.join([m['id'], m['title'], m['authorsYear']]) + suffix)
        sys.stdout.flush()

else:
    for line in sys.stdin:
        fields = line.rstrip().split('\t')
        suffix = '\t' + '\t'.join(fields)
        
        cmd=url + urllib.parse.quote(fields[0])
        j=requests.get(cmd, headers={"x-api-key": apikey}).json()
        # print(j, file=sys.stderr)
        print('# %d matches:\t' % len(j['matches']) + fields[0])
        for m in j['matches']:
            print('\t'.join([m['id'], m['title']]) + suffix)
        sys.stdout.flush()
    
