#!/bin/bash

for model in allenai/scibert_scivocab_cased; do
	
	for bin in {0..45..10} 99; do

		echo ${bin} ${model}
		
		python convert_torch_to_np.py \
			--bin_num ${bin} \
			--model_name ${model} \
			--experiment_name filter_newline \
			--sample_size 1000
	done

	python bin_summary_stats.py \
		--model_name ${model} \
		--experiment_name filter_newline \
		--sample_size 1000

	done