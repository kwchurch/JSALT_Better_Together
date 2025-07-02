#!/usr/bin/env python

import numpy as np
import torch
import argparse,sys,ast

from transformers import AutoModel, AutoTokenizer

# model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
# adapter_name = model.load_adapter("allenai/specter2", source="hf", set_active=True)

parser = argparse.ArgumentParser()
# parser.add_argument("--output", help='filename', required=True)
# parser.add_argument("--device", help='cuda|cpu', default='cpu')
parser.add_argument("--fields", help='comma separated fields to pull out of json inputs; if None, assume input is text', default=None)
parser.add_argument("--start", type=int, help='line to start on', default=0)
parser.add_argument("--end", type=int, help='line to end on', default=None)
parser.add_argument("--model", help='name of model on HuggingFace', required=True)
# parser.add_argument("--adapter", help='name of adapter on HuggingFace', default=None)
parser.add_argument("--sep", help='sep token', default='[SEP]')
parser.add_argument("--reconstitute", help="", action='store_true')
# parser.add_argument("--binary_output", help="output float32", action='store_true')

args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.model)
# model = AutoModel.from_pretrained(args.model)

# if not args.adapter is None:
#     # from adapters import AutoAdapterModel
#     model.load_adapter(args.adapter)

def unjsonify(s, fields):
    if fields is None: return str(s)
    j = ast.literal_eval(s)
    res = []
    for f in fields.split(','):
        try:
            if f in j and not j[f] is None:
                res.append(j[f].encode('unicode-escape').decode('ascii'))
        except:
            print('unable to find %s in %s' % (str(f), str(j)), file=sys.stderr)
    return args.sep.join(map(str,res))

lines = [unjsonify(line.rstrip(), args.fields) for line in sys.stdin]
end = args.end
if not end is None and end > len(lines): end = None
if end is None: end = len(lines)

if args.start < end: 
    for i, text in enumerate(lines[args.start:end]):
        try:
            tok = tokenizer(text)['input_ids']
            if args.reconstitute: print(tokenizer.decode(tok))
            else: print(tok)
            # print(tokenizer.decode(tokenizer(text)['input_ids']))
        except:
            print('*** Error *** on line: ' + str(i))
            # print(text.encode('unicode-escape').decode('ascii'))



