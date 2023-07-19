import numpy as np, os, sys
from tqdm import tqdm
import regex as re
from contextlib import ExitStack

if __name__ == '__main__':

	shard_to_check = int(sys.argv[1])
	output_dir = sys.argv[2]

	corpus_ids = []

	cid_pat = re.compile(r'\"corpusid\":([0-9]+)[,|}]')

	lines = 0
	matches = 0
	found = 0

	#Load id2bin
	id2bin = np.loadtxt(os.path.join(os.environ['JSALTdir'], 'semantic_scholar/j.ortega/corpusId_to_bin.txt'), dtype='int32')
	print('Done loading id2bin')
	id2bin_dict = {a[0] : a[1] for a in id2bin}


	with open(f'sampled_abstracts/{shard_to_check:03d}', 'r') as abstracts_file:
		
		with ExitStack() as stack:
			out_file_list = [stack.enter_context(open(f'{output_dir}{bin_id:03d}', 'w')) for bin_id in range(100)]

			for line in tqdm(abstracts_file):
				
				lines += 1
				match = re.findall(cid_pat, line)

				if match:
					cid = int(match[0])

					if cid in id2bin_dict:
						b = id2bin_dict[cid]
						out_file_list[b].write(line)
						found += 1

					matches += 1

	print(f'Sorted {matches} out of {lines} ({matches/lines}%) total read papers.')