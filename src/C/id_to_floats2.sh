#!/bin/sh

rel=2022-12-02
indir=/scratch/k.church/semantic_scholar/releases/$rel/database/embeddings

id_to_floats --binary_output --floats $indir/specter.kwc.edges.f --record_size 768 --map $indir/specter.kwc.nodes.txt 

