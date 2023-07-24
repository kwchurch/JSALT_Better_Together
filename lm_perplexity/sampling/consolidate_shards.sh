#!/bin/bash

shard_to_bin=shard_to_bin/
bin_write_dir=bin_samples/

mkdir -p ${bin_write_dir}

for bin in {0..99}
do
	printf -v bin_folder_name "%03d" ${bin}
	echo ${bin_folder_name}

	cat ${shard_to_bin}/*/${bin_folder_name} > ${bin_write_dir}${bin_folder_name}



done