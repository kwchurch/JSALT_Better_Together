#!/bin/bash

for model in bert-base-multilingual-cased; do
	
	for bin in {0..99..10} 99; do

		echo ${bin} ${model}
		
		python convert_torch_to_np.py \
			--bin_num ${bin} \
			--model_name ${model} \
			--experiment_name multilingual \
			--sample_size 1000
	done

	python bin_summary_stats.py \
		--model_name ${model} \
		--experiment_name multilingual \
		--sample_size 1000

	done