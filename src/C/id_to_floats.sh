#echo $id | $src/fetch_references_and_citations.py > /tmp/x_john
dir=/scratch/k.church/semantic_scholar/embeddings/new
K=768
ffile=$dir/specter.kwc.edges.f
map=/scratch/k.church/semantic_scholar/embeddings/specter.kwc.nodes.txt

id_to_floats --record_size $K --floats $ffile --map $map
#| sort -nr | find_lines --input /work/k.church/semantic_scholar/papers/papers2url.V2/lines2html.V2 --fields '--L'
