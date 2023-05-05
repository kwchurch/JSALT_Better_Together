#!/usr/bin/env python

import numpy as np
import sys,json,requests,os,time

apikey=os.environ.get('SPECTER_API_KEY')

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

def get_ids(my_id, attempt):
    j = requests.get('https://api.semanticscholar.org/graph/v1/paper/' + my_id + '?fields=externalIds',
                     headers={"x-api-key": apikey}).json()
    if 'externalIds' in j or attempt <= 0:
        return j
    else:
        time.sleep(attempt+1)
        return get_ids(my_id, attempt-1)

for line in sys.stdin:
    fields = line.rstrip().split('\t')
    my_id = id_ify(fields[0])

    j = get_ids(my_id, 1)

    # if len(fields) == 1: suffix = ''
    # else: suffix = '\t' + '\t'.join(fields[1:])

    suffix = '\t' + '\t'.join(fields)

    if 'externalIds' in j:
        print(my_id + '\t' + str(j['externalIds']['CorpusId']) + suffix)
    else:
        print(my_id + '\tNA' + suffix)
    sys.stdout.flush()
