#!/bin/bash

sampled_abstracts_dir=sampled_abstracts/

main_write_dir=shard_to_bin/
printf -v shard_to_check "%03d" ${1}

mkdir -p ${main_write_dir}${shard_to_check}

write_dir=${main_write_dir}${shard_to_check}/



echo writing to ${write_dir}

python sample_to_bin.py ${shard_to_check} ${write_dir}

