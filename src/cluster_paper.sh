#!/bin/sh

embedding=proposed

if [ $# -ge 2 ]
then
embedding=$2
fi

tmp=/tmp/cluster_paper.$$

if [ "$embedding" == "proposed" ]
then
K=280
dir=/work/k.church/semantic_scholar/citations/graphs/K$K/papers/
ffile=$dir/citations.npz.papers.kwc.edges.f
map=$dir/map
elif [ $embedding == "specter" ]
then
dir=/work/k.church/semantic_scholar/releases/2022-12-02/database/embeddings
K=768
ffile=$dir/specter.kwc.edges.f
map=$dir/specter.kwc.nodes.txt
else
echo unknown embedding $embdding
exit 1
fi


echo $1 | $src/fetch_references_and_citations.py |
awk '/ERROR/ {next}; $1 == "reference" {print $2; print $3}' | awk 'killroy[$1]++ < 1' |
id_to_floats --floats $ffile --record_size $K --map $map |
$src/cluster_paper.py |
find_lines --input /work/k.church/semantic_scholar/papers/papers2url.V2/lines2html.V2 --fields '-----L'




