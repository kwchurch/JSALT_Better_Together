#!/usr/bin/env python

import sys,json,os,argparse,gzip,ast,time

t0=time.time()

errors = 0

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="filename", required=True)
parser.add_argument("-o", "--output", help="filename", default=None)
parser.add_argument("--id", help="name of id field", default='corpusid')
args = parser.parse_args()

slurm=os.environ.get('SLURM_ARRAY_TASK_ID')

if '%' in args.input and not slurm is None:
    input_file = args.input % int(slurm)
else:
    input_file = args.input

if args.output is None:
    output_fd = sys.stdout
    output_file = '-'
elif '%' in args.output and not slurm is None:
    output_file = args.output % int(slurm)
    output_fd = open(output_file, 'w')
else:
    output_file = args.output
    output_fd = open(output_file, 'w')

print('input: ' + str(input_file), file=sys.stderr)
print('output: ' + str(output_file), file=sys.stderr)
print('id: ' + str(args.id), file=sys.stderr)

with gzip.open(input_file) as input_fd:
        for line in input_fd:
            try:
                jj = json.loads(line)
                # jj = ast.literal_eval(line)
                id = str(jj[args.id])
                print(id, file=output_fd)
            except:
                errors += 1

print('%d errors' % errors, file=sys.stderr)
print('done: ' + str(time.time() - t0), file=output_fd)



