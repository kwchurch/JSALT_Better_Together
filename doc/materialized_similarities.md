# Materialized Similarities

Let M be an embedding (from specter, specter2, scincl, proposed,
etc.).  We cannot afford to materialize M@M.T, but we can compute
many of the large values in M@M.T, using the indexes for approximate nearest neighbors.
<p>
Each index, pi, is a permutation of N ints such that paper ids that are "close in pi" have large
cosines in M.  We have an offset arg to determine "close in pi".
Note that there are only N ints in pi, so we only need to compute offset*N cosines in M for each index.
<p>
We have materialized the big values for four embeddings (as of now):

```sh
du -h $JSALTdir/semantic_scholar/embeddings/*/bigrams | sort -nr
# 424G	/work/k.church/JSALT-2023//semantic_scholar/embeddings/specter/bigrams
# 399G	/work/k.church/JSALT-2023//semantic_scholar/embeddings/proposed/bigrams
# 186G	/work/k.church/JSALT-2023//semantic_scholar/embeddings/scincl/bigrams
# 109G	/work/k.church/JSALT-2023//semantic_scholar/embeddings/specter2/bigrams
```

The bigram files are sequences of floats and two ints (sorted by the two ints).
The two ints are corpusIds and the float is a cosine score.


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

<p>

The following selects bigrams with large cosines from proposed and outputs
their scores in a number of embeddings.  (Note: cosine of -1 means NA).

```sh
$JSALTsrc/C/print_bigrams $proposed/bigrams | sed 1000000q | awk 'rand() < 1/100000' | cut -f2- | head | $JSALTsrc/pairs_to_cos.sh
# proposed	scincl	specter2	specter	specter.K280
# 0.997	-1.000	-1.000	0.485	0.477	751	14590501
# 0.974	0.756	0.856	0.603	0.601	2178	15189611
# 0.972	0.932	-1.000	0.830	0.851	1269	42117050
# 0.970	0.815	0.847	0.483	0.500	1303	7285822
# 0.928	0.876	0.897	0.778	0.777	2047	23454356
# 0.912	0.835	0.906	0.660	0.644	1073	235321971
# 0.902	-1.000	-1.000	0.314	0.167	162	62174086
# 0.891	0.777	0.864	0.348	0.328	1889	215914730
# 0.876	-1.000	-1.000	-1.000	-1.000	183	192532181
# 0.856	-1.000	-1.000	0.657	0.632	1948	18721980
```

Same as the above, but we select bigrams with large cosines from scincl.  Thus, the first column has large cosines above,
and the second column has large cosines below.

```sh
$JSALTsrc/C/print_bigrams $scincl/bigrams | sed 1000000q | awk 'rand() < 1/100000' | cut -f2- | head | $JSALTsrc/pairs_to_cos.sh
# proposed	scincl	specter2	specter	specter.K280
# 0.906	0.828	0.882	0.681	0.697	551	8392719
# 0.754	0.873	0.915	0.584	0.592	3982	7278363
# 0.349	0.919	0.891	0.791	0.796	8294	38958396
# 0.169	0.741	-1.000	0.412	0.418	7429	144146979
# 0.123	0.841	0.888	0.485	0.448	4873	147428608
# 0.070	0.758	0.790	0.512	0.549	7243	95907927
# 0.027	0.749	0.870	0.247	0.313	2775	164865317
# 0.016	0.830	0.855	0.533	0.548	7825	119957307
# 0.014	0.780	0.832	0.516	0.494	486	210163984
# -0.006	0.807	0.883	0.680	0.726	5028	167748753
```

