# lookup by vectors

The following depends on some env variables ($JSALTdir refers to <a
href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2F">Globus</a>)

```sh
export specter=$JSALTdir/semantic_scholar/embeddings/specter
export specter2=$JSALTdir/semantic_scholar/embeddings/specter2
export proposed=$JSALTdir/semantic_scholar/embeddings/proposed
export scincl=$JSALTdir/semantic_scholar/embeddings/scincl
export LinkBERT=$JSALTdir/semantic_scholar/embeddings/LinkBERT
```

Fast lookup


```sh
query=3051291
echo $query |
$JSALTsrc/C/x_to_y ai | 
$JSALTsrc/C/extract_row $proposed/bigrams |
$JSALTsrc/C/print_bigrams | 
sort -nr | head 
# 1.00	3051291	8399404
# 1.00	3051291	54448357
# 1.00	3051291	3958144
# 1.00	3051291	3952914
# 1.00	3051291	3951790
# 1.00	3051291	3919301
# 1.00	3051291	2452205
# 1.00	3051291	207238980
# 1.00	3051291	13999578
# 0.99	3051291	9661057
```

Same as above but outputs a json object
for each result in the last column.

```sh
query=3051291
echo $query |
$JSALTsrc/C/x_to_y ai | 
$JSALTsrc/C/extract_row $proposed/bigrams |
$JSALTsrc/C/print_bigrams | 
sort -nr | head | 
cut -f3 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields year,citationCount,title
```

The following looks up papers by in 3 indices

```sh
echo $query | $JSALTsrc/C/near_with_floats --offset 3 --dir $proposed $proposed/idx.1[012].i
```

The following gets a vector:

```sh
echo $query | $JSALTsrc/C/id_to_floats --dir $proposed | tr ' ' '\n' | awk 'NR >= 3' | x_to_y af > /tmp/vec
```

Lookup by vector in 10 indices:

```sh
$JSALTsrc/C/vector_near_with_floats --offset 5 --dir $proposed $proposed/idx.1?.i <  /tmp/vec 
```

Same as above, but returns a json object for each candidate

```sh
$JSALTsrc/C/vector_near_with_floats --offset 5 --dir $proposed $proposed/idx.1?.i <  /tmp/vec | 
cut -f2- | tr '\t' '\n' | sort -u | 
$JSALTsrc/fetch_from_semantic_scholar_api.py --fields year,title
```
