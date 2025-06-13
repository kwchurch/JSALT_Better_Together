#!/usr/bin/env python

import numpy as np
import torch
import argparse,sys,ast,time

from transformers import (AutoModel, AutoTokenizer)

# model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
# adapter_name = model.load_adapter("allenai/specter2", source="hf", set_active=True)

t0 = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--output", help='filename', required=True)
parser.add_argument("--device", help='cuda|cpu', default='cpu')
parser.add_argument("--fields", help='comma separated fields to pull out of json inputs; if None, assume input is text', default=None)
parser.add_argument("--start", type=int, help='line to start on', default=0)
parser.add_argument("--end", type=int, help='line to end on', default=None)
parser.add_argument("--model", help='name of model on HuggingFace', required=True)
parser.add_argument("--adapter", help='name of adapter on HuggingFace', default=None)
parser.add_argument("--sep", help='sep token', default='[SEP]')
parser.add_argument("--binary_output", help="output float32", action='store_true')

args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModel.from_pretrained(args.model)

if not args.adapter is None:
    # from adapters import AutoAdapterModel
    model.load_adapter(args.adapter)

model = model.to(args.device)

def get_HF_embeddings(batch_texts):
    inference_batch_size = 32
    err=0
    if args.binary_output: fd = open(args.output, 'wb')
    
    embeddings = []
    for i in range(0, len(batch_texts), inference_batch_size):
        sub_batch = batch_texts[i:i + inference_batch_size]
        
        # inputs = torch.tensor([tokenizer.encode(line, padding=True, truncation=True, return_tensors="pt", max_length=512) for line in sub_batch])

        inputs = tokenizer(sub_batch, padding=True, truncation=True,
                           return_tensors="pt", max_length=512)

        inputs = {k: v.to(args.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            try:
                outputs = model(**inputs)
                sub_batch_embeddings = outputs.last_hidden_state[:, 0, :]

                emb = sub_batch_embeddings.cpu().numpy()
                if args.binary_output:
                    x = np.array(emb)
                    x.astype(np.float32).tofile(fd)
                    fd.flush()
                    print('%0.0f seconds: i = %d, x.shape = %s' % (time.time() - t0, i, str(x.shape)), file=sys.stderr)
                    sys.stderr.flush()
                else:            
                    embeddings.append(emb)
            except:
                err += 1

    if not args.binary_output:
        np.save(args.output, np.vstack(embeddings))

    return err


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

def old_unjsonify(s, fields):
    if fields is None: return s
    j = ast.literal_eval(s)
    res = []
    for f in fields.split(','):
        try:
            if f in j and not j[f] is None:
                res.append(j[f])
        except:
            print('unable to find %s in %s' % (str(f), str(j)), file=sys.stderr)
    return args.sep.join(map(str,res))

lines = [unjsonify(line.rstrip(), args.fields) for line in sys.stdin]
end = args.end
if not end is None and end > len(lines): end = None
if end is None: end = len(lines)

if args.start < end: 
    errors = get_HF_embeddings(lines[args.start:end])
    print('done: ' + str(time.time() - t0) + ' seconds', file=sys.stderr)
    print(str(errors) + ' errors', file = sys.stderr)
