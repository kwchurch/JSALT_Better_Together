
import sys,json,ast

def clean(x):
    return str(x).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

for line in sys.stdin:
    j = ast.literal_eval(line.rstrip())
    print('\t'.join(map(clean, [j[i] for i in sys.argv[1:]])))
