#!/usr/bin/env python

import sys,json

# lines = sys.stdin.read().split('\n')
# print(str(len(lines)-1) +  ' 768')
for line in sys.stdin:
    rline = line.rstrip()
    if len(rline) > 1:
        j = json.loads(rline)
        v = str(j['vector'])
        v = v.replace(',', '')
        v = v.replace('[', '')
        v = v.replace(']', '')
        print('corpusid_' +  str(j['corpusid']) + ' ' + v)

