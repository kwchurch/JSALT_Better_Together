#!/usr/bin/env python

import sys,json,requests


def id_ify(s):
    if len(s) == 40: return s
    for prefix in ['CorpusId:', 'PMID:', 'ACL:', 'arXiv:', 'DOI:']:
        if s.startswith(prefix):
            return s

    fields = s.split('/')

    if s.startswith('https://doi.org/') and fields[-1].startswith('arXiv.'):
        p='arXiv:'
        return p + fields[-1][len(p):]

    p = '/doi/'
    pp = s.find(p)
    print('pp = ' + str(pp), file=sys.stderr)
    if pp >= 0:
        pieces = s[pp + len(p):].split('/')
        return 'DOI:' + pieces[-2] + pieces[-1].split('?')[0]

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

keyword='<title>'
for line in sys.stdin:
    try:
        fields = line.rstrip().split('\t')
        txt = requests.get(fields[0]).text
        p0 = txt.find(keyword) + len(keyword)
        title = 'NA'
        p1 = txt.find('</title>')
        if p0 >= 0 and p1 >=0:
            title = txt[p0:p1].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    except:
        title = 'NA'
    print(title + '\t' + '\t'.join(fields))
    sys.stdout.flush()
