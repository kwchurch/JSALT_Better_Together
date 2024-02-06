#!/usr/bin/env python

import json,requests,argparse,struct
import os,sys,argparse,time
import numpy as np

t0 = time.time()

print('lookup_paper_in_bigrams: ' + str(sys.argv), file=sys.stderr)

apikey=os.environ.get('SPECTER_API_KEY')

# assumes the dir argument contains
#   embedding.f  sequence of N by K floats32
#   map.old_to_new.i  sequence of N int32
#   record_size  specifies K

parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="a directory such as $proposed or $specter", required=True)
parser.add_argument("--topN", type=int, help="top N results to return", default=10)
parser.add_argument('--fields', help="fields to pass to Semantic Scholar API", default=None)
args = parser.parse_args()

def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')

def truncate_candidates(cand):
    if len(cand) > args.topN:
        return cand[0:args.topN]
    return cand

bigrams_idx = bigrams_file = None
bigrams_file = args.dir + '/bigrams'
bigrams_idx = map_int64(bigrams_file + '.idx')

def lookup_paper_in_bigrams_file(query):
    if query < 0: return []
    if query+1 >= len(bigrams_idx):
        print('lookup_paper: query (%d) exceeds len(idx) (%d)' % (query, len(bigrams_idx)), file=sys.stderr)
        return []
    start = bigrams_idx[query]
    end = bigrams_idx[query+1]
    nbytes = 12*(end - start)
    with open(bigrams_file, 'rb') as fd:
        fd.seek(start * 12)
        bytes = fd.read(nbytes)
        res = truncate_candidates(sorted([record for record in struct.iter_unpack('fii', bytes)], key=lambda rec: rec[0], reverse=True))
        return res

def safe_lookup(id, f, dict):
    if id in dict and f in dict[id]:
        return dict[id][f]
    else: return None

if not args.fields is None:
    print('score\tid1\tid2\t' + args.fields.replace(',', '\t'))

for line in sys.stdin:
    rline = line.rstrip()
    fields = rline.split()
    if len(fields) < 1: continue

    res = lookup_paper_in_bigrams_file(int(fields[0]))

    if args.fields is None:
        for score,id1,id2 in res:
            print('\t'.join(map(str,[score, id1, id2])))

    else:
        sfields = args.fields.split(',')
        # print('sfields: ' + str(sfields), file=sys.stderr)
        S2_res = {}
        ids = ['CorpusId:' + str(id2) for score,id1,id2 in res]
        r = requests.post(
            'https://api.semanticscholar.org/graph/v1/paper/batch',
            params={'fields': 'externalIds,' + args.fields},
            json={"ids": ids},
            headers={"x-api-key": apikey}).json()
        print(r, file=sys.stderr)
        for rec in r:
            # print('rec: ' + str(rec), file=sys.stderr)
            if rec is None: continue
            if not 'externalIds' in rec: continue
            k = rec['externalIds']['CorpusId']
            if not k in S2_res:
                S2_res[k] = {}
            for f in sfields:
                if f in rec:
                    S2_res[k][f] = rec[f]

        # print('S2_res: ' + str(S2_res), file=sys.stderr)
        for score,id1,id2 in res:
            vals = '\t'.join(map(str,[ safe_lookup(id2, f, S2_res) for f in sfields]))
            print('\t'.join(map(str,[score, id1, id2, vals])))


print('%0.0f sec: done' % (time.time() - t0), file=sys.stderr)
