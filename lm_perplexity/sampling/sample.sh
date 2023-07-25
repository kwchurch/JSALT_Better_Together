#! /bin/bash

sample_dir=/rc_scratch/abeb4417/jsalt/semantic_scholar/releases/2023-06-20/database/abstracts/
write_dir=sampled_abstracts/

mkdir -p ${write_dir}

printf -v shard "%03d" $1
echo ${sample_dir}abstracts.piece."$shard".gz

zcat ${sample_dir}abstracts.piece."$shard".gz | perl -n -e 'print if (rand() < 0.075)' >> ${write_dir}"${shard}"




