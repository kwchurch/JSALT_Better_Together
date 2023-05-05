#!/usr/bin/env python

import numpy as np
import pandas as pd
import sys,argparse,os
from S2search import S2paperAPI

apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="query", required=True)
parser.add_argument("-f", "--fields", help="comma separated values", default="corpusId,title,year,citationCount")
parser.add_argument("-N", "--topN", type=int, help="number of return values", default=10)
parser.add_argument("-s", "--sort", help="total-citatations|influence|pub-date|relevance", default='total-citations')

args = parser.parse_args()

k = S2paperAPI()
k.get(args.query, n=args.topN, fields=args.fields.split(','), sort=args.sort)


for i in range(k.all.shape[0]):
    print('\t'.join(map(str,[k.all[col][i] for col in k.all])))

