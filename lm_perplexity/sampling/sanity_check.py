import numpy as np, sys, regex as re


if __name__ == '__main__':

	id2bin = np.loadtxt('/rc_scratch/abeb4417/jsalt/semantic_scholar/j.ortega/corpusId_to_bin.txt', dtype='int32')

	mapper = np.zeros(np.max(id2bin[:,0]) + 1, dtype='int32')
	mapper[id2bin[:,0]] = id2bin[:,1]

	sample_dir = 'bin_samples/'
	cid_pat = re.compile(r'\"corpusid\":([0-9]+)[,|}]')

	for bin_i in range(100):
		cids = []
		
		with open(f'{sample_dir}{bin_i:03d}', 'r') as f:
			for line in f:
				cids.append(int(re.findall(cid_pat, line)[0]))

		bins = np.unique(mapper[np.asarray(cids)])
		print(f'Bin {bin_i} : {bins}')




	


