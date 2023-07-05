import os, sys, requests, random, pandas
from tqdm import tqdm, trange

from joblib import Memory

cache_dir = '/rc_scratch/abeb4417/joblib_cache/'
memory = Memory(cache_dir, verbose=1)


def fetch_semantic_scholar_info(corpus_ids = [], paper_ids = [], fields="title,abstract,externalIds,corpusId", max_batch_size=500, output_file = None, verbose=False):

	processed_ids = processed_ids = ['CorpusId:{}'.format(id) for id in corpus_ids] + paper_ids

	returned_objects = {}

	for i in trange(0,len(corpus_ids)+1,max_batch_size):
		to_send = processed_ids[i:i+max_batch_size]

		if len(to_send) == 0:
			continue
	
		if verbose:
			print('Sending following IDS to Semantic Scholar (len {}): {}'.format(len(processed_ids), processed_ids))

		apikey=os.environ.get('SPECTER_API_KEY')
		r = requests.post(
			'https://api.semanticscholar.org/graph/v1/paper/batch',
			params={'fields': fields},
			headers={"x-api-key" : apikey},
			json={"ids" : to_send}
		)

		for resp in r.json():
			if resp is not None and isinstance(resp, dict):
				returned_objects[resp['corpusId']] = resp


	if output_file:
		with open(output_file, 'w') as f:
			json.dump(r.json(), f, indent=2)

	return returned_objects

def fetch_references(corpus_id, fields="title,authors,referenceCount,citationCount,references,references.title,citations,citations.title", output_file=None):


	processed_id = f'CorpusId:{corpus_id:s}'
	apikey=os.environ.get('SPECTER_API_KEY')

	r = requests.get(
		f'https://api.semanticscholar.org/graph/v1/paper/{processed_id:s}',
		params={'fields' : fields},
		headers={"x-api-key" : apikey}
	)

	return r.json()


def get_bin_ids(bin_num, subgraph_dir, return_int=True):


	bin_file = os.path.join(subgraph_dir, f'{bin_num:03d}')
	with open(bin_file, 'r') as f:
		if return_int:
			ids = [int(line.strip()) for line in f]
		else:
			ids = [line.strip() for line in f]

	return ids

def get_all_previous_bin_ids(curr_bin, subgraph_dir):

	id_to_bin = {}

	for i in trange(0,curr_bin):
		bin_ids = get_bin_ids(i, subgraph_dir)
		for bid in bin_ids:
			id_to_bin[bid] = i

	return id_to_bin		

def unify_bin_to_bin(dir='bin_to_bin/'):

	df_list = []

	for i in range(100):
		fname = os.path.join(dir, f'bin_{i}_-1_42.tsv')
		if os.path.exists(fname):
			df_list.append(pandas.read_csv(fname, sep='\t'))
	
	df = pandas.concat(df_list)
	df.to_csv('joint_b2b_counts.tsv', sep='\t')


if __name__ == '__main__':

	unify_bin_to_bin()