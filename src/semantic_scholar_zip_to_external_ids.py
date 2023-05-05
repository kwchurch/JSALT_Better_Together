#!/usr/bin/env python

import sys,json,os,argparse,gzip,ast,time

t0=time.time()

errors = 0

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename", required=True)
parser.add_argument("-o", "--output", help="filename", default=None)
# parser.add_argument("--id", help="name of id field", default='corpusid')
args = parser.parse_args()

slurm=os.environ.get('SLURM_ARRAY_TASK_ID')

if '%' in args.input and not slurm is None:
    input_file = args.input % int(slurm)
else:
    input_file = args.input

# {"ACL":null,"DBLP":null,"ArXiv":null,"MAG":null,"CorpusId":"202724712","PubMed":null,"DOI":null,"PubMedCentral":null}

externalIds = ['ACL', 'DBLP', 'ArXiv', 'MAG', 'CorpusId', 'PubMed', 'DOI', 'PubMedCentral']

if args.output is None:
    assert False, 'should not happen'
    output_fd = sys.stdout
elif '%' in args.output and not slurm is None:
    output_file = args.output % int(slurm)
    # output_fd = open(output_file, 'w')
else:
    output_file = args.output
    # output_fd = open(output_file, 'w')

output_fds = {}
for id in externalIds:
    output_fds[id] = open(output_file + '.' + id, 'w')

print('input: ' + str(input_file), sys.stderr)
print('output: ' + str(output_file), sys.stderr)
# print('id: ' + str(args.id), sys.stderr)

with gzip.open(input_file) as input_fd:
        for line in input_fd:
            try:
                jj = json.loads(line)
                ids = jj['externalids']
                if not ids is None:
                    corpusid = ids['CorpusId']
                    for id in ids:
                        if not ids[id] is None:
                            print(corpusid, file=output_fds[id])
            except:
                errors += 1

print('%d errors' % errors, file=sys.stderr)
print('done: ' + str(time.time() - t0), file=output_fd)



