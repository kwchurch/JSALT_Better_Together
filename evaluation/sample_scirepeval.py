from datasets import load_dataset
import random, pandas, os, sys

def sample_scirepeval(task, split='evaluation', sample_size=200, seed=42, output_folder='scirepeval_sample/'):

	dataset = load_dataset('allenai/scirepeval', name=task, split=split)
	print('Size of evaluation dataset: {}'.format(len(dataset)))

	dataset = dataset.shuffle(seed=seed)
	dataset_subset = dataset[:sample_size]

	df_dataset = pandas.DataFrame(dataset_subset)
	df_dataset.to_csv(os.path.join(output_folder, 
					'{task}_{split}_{orig_size}_{seed}_{size}.tsv'.format(
						task=task,
						split=split,
						orig_size=len(dataset),
						seed=seed,
						size=sample_size
					)),
					sep='\t')


def main():
	

	tasks_to_load = ['fos', 'mesh_descriptors', 'cite_count', \
	 'pub_year', 'cite_prediction', 'cite_prediction_new', \
	 'high_influence_cite', 'same_author', 'search', 'biomimicry', \
	 'drsm', 'feeds_1', 'feeds_m', 'feeds_title', 'peer_review_score_hIndex', \
	 'trec_covid', 'tweet_mentions', 'scidocs_mag_mesh', \
	 'scidocs_view_cite_read', 'paper_reviewer_matching']

	total_splits = int(sys.argv[1])
	current_split = int(sys.argv[2])

	print('Sampling SRE using split {} of {}.'.format(current_split, total_splits))

	split_size = len(tasks_to_load) // total_splits
	start_location = current_split * split_size

	split = tasks_to_load[start_location:start_location + split_size]

	for task in split:
		sample_scirepeval(task)



if __name__ == '__main__':

	main()