#!/usr/bin/env python

import sys,json,gzip #,langdetect
# from ftlangdetect import detect

import cld3

for line in sys.stdin:
    print(str(len(line)) + '\t' + '\t'.join(map(str, cld3.get_language(line))))

