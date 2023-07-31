#!/usr/bin/env python

import sys,os,struct,argparse
import numpy as np
import numpy.linalg
import sklearn.linear_model

# print(sys.argv, file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="text file with two columns", required=True)
parser.add_argument('--guess_when_missing', action='store_true')
args = parser.parse_args()

x = np.loadtxt(args.input)
X = x[:,1]
Y = x[:,0] < 1.5

if args.guess_when_missing:
    s = (X < -0.9)
    p = np.mean(s)
    print('p: ' + str(p), file=sys.stderr)
    if p < 0: p=0
    if p > 1: p=1
    guesses = np.random.choice(2, size=(np.sum(s)), p = [1-p, p])
    # print(guesses, file=sys.stderr)
    X[s] = guesses

model = sklearn.linear_model.LogisticRegression()
model.fit(X.reshape(-1,1), Y)
predictions = model.predict_proba(X.reshape(-1,1))
norm1 = np.linalg.norm(predictions, axis=1)
best = np.argmin(norm1)
print('threshold: ' + str(X[best]))
