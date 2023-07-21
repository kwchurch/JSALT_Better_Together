#!/bin/bash

python convert_torch_to_np.py \
	--bin_num 0 \
	--model_name roberta-base \
	--experiment_name check \
	--sample_size 500

python bin_summary_stats.py \
	--model_name roberta-base \
	--experiment_name check \
	--sample_size 500