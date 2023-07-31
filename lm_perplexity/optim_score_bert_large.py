import os, sys, argparse, orjson, torch, numpy as np, regex as re

from tqdm import tqdm, trange

from transformers import AutoModelForMaskedLM, AutoTokenizer

def get_inputs(input_ids, vocab_size, max_len):

	x = torch.tensor(input_ids + [tokenizer.pad_token_id] * (args.max_seq_len - len(input_ids)))
	attention_mask = torch.tensor([1] * len(input_ids) + [0] * (args.max_seq_len - len(input_ids)))
	attention_mask = attention_mask.repeat(attention_mask.shape[-1], 1)

	repeats = x.repeat(x.shape[-1], 1)
	mask = torch.ones(x.shape[-1]).diag(0)

	masked_input = repeats.masked_fill(mask == 1, tokenizer.mask_token_id)
	labels = repeats.masked_fill(masked_input != tokenizer.mask_token_id, -100)

	return x, masked_input, labels, attention_mask

if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('--bin_num', type=int)
	parser.add_argument('--model_name', type=str)
	parser.add_argument('--experiment_name', type=str)
	parser.add_argument('--sample_size', type=int, default=10000)
	parser.add_argument('--batch_size', type=int, default=32)
	parser.add_argument('--max_seq_len', type=int, default=128)
	parser.add_argument('--bin_samples_dir', type=str, default='sampling/bin_samples/')
	parser.add_argument('--write_dir', type=str, default='log_calculations/torch_outputs/')
	parser.add_argument('--local_model_dir', type=str, default='log_calculations/pretraining/')
	parser.add_argument('--local_experiment_name', type=str)
	parser.add_argument('--local_model_name', type=str)
	parser.add_argument('--local_model_checkpoint', type=str, default='final_model/')
	parser.add_argument('--use_local_model', action='store_const', const=True, default=False)
	parser.add_argument('--strip_newlines', action='store_const', const=True, default=False)
	parser.add_argument('--index_only', action='store_const', const=True, default=False, help='Do not calculate scores, only update the index.')

	args = parser.parse_args()

	abstracts = []
	cids = []

	whitespace_pat = re.compile(r'[\n|\t|\s]+')

	with open(os.path.join(args.bin_samples_dir, f'{args.bin_num:03d}')) as input_sample:
		for line in input_sample:
			dat = orjson.loads(line)
			abstract = dat['abstract']

			if args.strip_newlines:
				abstract = re.sub(whitespace_pat, ' ', abstract)

			cids.append(dat['corpusid'])
			abstracts.append(abstract)

			if len(abstracts) >= args.sample_size:
				break

	tokenizer = AutoTokenizer.from_pretrained(args.model_name)
	tokenized_abstracts = tokenizer(abstracts, truncation=True, max_length=args.max_seq_len)['input_ids']

	masked_inputs = []
	padded_inputs = []
	labels = []
	attention_masks = []
	lengths = []

	for inpid in tqdm(tokenized_abstracts):
		padded_input, masked_input, label, attention_mask = get_inputs(inpid, tokenizer.vocab_size, args.max_seq_len)
		padded_inputs.append(padded_input)
		masked_inputs.append(masked_input)
		labels.append(label)
		attention_masks.append(attention_mask)
		lengths.append(len(inpid))

	if args.use_local_model:
		model_write_dir = os.path.join(args.write_dir, args.experiment_name, args.local_model_name, args.model_name)
		
	else:
		model_write_dir = os.path.join(args.write_dir, args.experiment_name, f'{args.model_name}')
	print(f'Generated model_write_dir: {model_write_dir}')
	if not os.path.exists(model_write_dir):
		os.makedirs(model_write_dir)

	# Index checks

	if len(cids) != len(abstracts):
		print('cid != abstracts')
	if len(tokenized_abstracts) != len(abstracts):
		print('tokens != abstracts')

	with open(os.path.join(model_write_dir, f'{args.bin_num}_index.tsv'), 'w') as f:
		for cid, abstract, tokens in zip(cids, abstracts, tokenized_abstracts):
			f.write(f'{cid}\t{abstract}\t{tokens}\n')

	if args.index_only:
		print('Index only set. Not scoring inputs. ')
		quit(0)

	if args.use_local_model:
		model_name = os.path.join(args.local_model_dir, args.local_experiment_name, args.model_name, args.local_model_name, args.local_model_checkpoint)
		print(f'Attempting to load: {model_name}')
		model = AutoModelForMaskedLM.from_pretrained(model_name)
	else:
		print(f'Attempting to load: {args.model_name}')
		model = AutoModelForMaskedLM.from_pretrained(args.model_name)

	model = model.to('cuda:0')

	sm = torch.nn.Softmax(dim=2)

	num_batches = args.max_seq_len // args.batch_size

	pidx_seq_range = torch.arange(0,args.max_seq_len).unsqueeze(1)
	pidx_batch_range = torch.arange(0,args.batch_size).repeat(num_batches).unsqueeze(1)


	pidx_base = torch.hstack((pidx_batch_range, pidx_seq_range))
	pidx_base = pidx_base.to('cuda:0')

	probs = []

	for inp, label, raw_tokens, attn_mask, length, padded_input in tqdm(zip(masked_inputs, labels, tokenized_abstracts, attention_masks, lengths, padded_inputs), total=len(labels)):

		inp = inp.to('cuda:0')
		attn_mask = attn_mask.to('cuda:0')

		pidx_s = padded_input.unsqueeze(1).to('cuda:0')
		pidx = torch.hstack((pidx_base[:len(pidx_s)], pidx_s))

		inp_batches = inp.split(args.batch_size, dim=0)
		pidx_batches = pidx.split(args.batch_size, dim=0)
		am_batches = attn_mask.split(args.batch_size, dim=0)

		batch_probs = []

		for bidx in range(num_batches):
			with torch.inference_mode():
				logits = model(inp_batches[bidx], attention_mask=am_batches[bidx]).logits
				prob = sm(logits)
				taken_probs = prob[pidx_batches[bidx][:,0],pidx_batches[bidx][:,1],pidx_batches[bidx][:,2]]
				
				batch_probs.append(torch.log(taken_probs).cpu())

		probs.append(torch.cat(batch_probs)[1:length-1])


	torch.save(probs, os.path.join(model_write_dir, f'{args.bin_num}_log_probs.pt'))

	#Checks

	for inp_ids, prob in zip(tokenized_abstracts, probs):
		if len(inp_ids) != prob.shape[0] + 2:
			print('error')
		
	