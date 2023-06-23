#!/bin/sh

for id in `cat ids.txt`
do
mkdir -p $id
echo $id | $JSALTsrc/fetch_references_and_citations.py > $id/one_hop.txt
$JSALTsrc/near.sh $id 20 | $JSALTsrc/tsv_to_html.sh > $id/$id.md
done
