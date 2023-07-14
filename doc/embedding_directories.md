# Embedding directories

<h2>Precomputed embeddings</h2>
  	    
This file explains what you can do with directories with precomputed embeddings.
Some examples of precomputed embedding directories are:
<ol>
<li>proposed</li>
<li>specter</li>
<li>specter.K280: like above but downsampled from K=786 to K=280, using random projections</li>
<li>specter2</li>
<li>scincl</li>
<li>LinkBERT</li>
<li>proposed/bins/[0-9][0-9][0-9]: We have split the 200M corpus ids by time into 100 bins with 2M ids each.  We are computing an embedding for each bin (though this is still a work in progress).</li>
<li>proposed/bins/prone.baseline/[0-9][0-9][0-9]: Similar to above, but using a different code base.   We are still trying to figure out why these cosines are slightly different from above.</li>
</ol>

It is assumed that each of these directories contain the following files:
<ol>
<li>embedding.f: a sequence of N by K floats, where N is the number of nodes (papers) in the embedding, and K is the number of hidden dimensions</li>
<li>record_size: defines a few configuration variables such as K (number of hidden dimensions) and B (number of random bytes in approximate neareast neighbors)</li>
<li>record_size.sh: similar to above</li>
<li>map.old_to_new.i: mappings between corpus ids (old) and offsets into embedding.f (new)</li>
<li>map.new_to_old.i: inverse of above</li>
<li>idx.*.i: permutation of N, used in approximate nearest neighbors.  Papers that are near one another in the permutation should have large cosines.</li>
<li>idx.*.i.inv: inverse of above</li>
</ol>

Many of these directories also have some other useful files:
<ol>
<li>proposed/bins/*/*new_pairs: text files with pairs of corpus ids and cosine scores</li>
<li>bigrams: similar to above, but binary files, sorted (without dups) </li>
</ol>

<h2>Environment Variables</h2>

For those of you with access to the Northeastern Cluster, you can find these files here.
For everyone else, the (small) files under $JSALTsrc are available on the <a href="https://github.com/kwchurch/JSALT_Better_Together/tree/main/src">GitHub</a>,
and the (large) files under $JSALTdir are avilable on <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2F">Globus</a>.
<p>
Unfortunately, the files under /scratch/k.church are not available to people outside of Northeastern.  We have a lot of space on /scratch, but
those files will be deleted soon, so those files should not be used for archival purposes.
<p>
If you have access to Northeastern Cluster, use these settings of the environment variables.
If not, download the files of interest from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2F">Globus</a> and set these variables appropriately to your local copy.

```sh
export JSALTdir=/work/k.church/JSALT-2023/
export JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

export specter=$JSALTdir/semantic_scholar/embeddings/specter
export specter2=$JSALTdir/semantic_scholar/embeddings/specter2
export proposed=$JSALTdir/semantic_scholar/embeddings/proposed
export scincl=$JSALTdir/semantic_scholar/embeddings/scincl
export LinkBERT=$JSALTdir/semantic_scholar/embeddings/LinkBERT

scratchProposed=/scratch/k.church/JSALT-2023/semantic_scholar/embeddings/proposed
scratchSpecter=/scratch/k.church/JSALT-2023/semantic_scholar/embeddings/specter
scratchSpecter2=/scratch/k.church/JSALT-2023/semantic_scholar/embeddings/specter2
scratchScincl=/scratch/k.church/JSALT-2023/semantic_scholar/embeddings/scincl
scratchLinkBERT=/scratch/k.church/JSALT-2023/semantic_scholar/embeddings/LinkBERT
```

<h2>What can we do with precomputed embeddings?</h2>

<ol>
<li><a href="#pairs2cos">pairs -> cos</a>: input pairs of corpus ids, output cosines</li>
<li><a href="#query2pairs">query -> pairs</a>: input query (a single corpus id), output cosines(</li>
<li><a href="#ids2vectors">ids -> vectors</a>: input corpus ids (one per line), output vectors (one per line); each vector starts with two ids and is then followed by K floats</li>
<li><a href="#vector2pairs">vector -> pairs</a>: input query (a vector, not necessarily in the embedding), output corpus ids and cosines of each id with query(</li>
<li><a href="@materialized">Materialized Similarities</a>: Many of the large values in M M^T have been precomputed, for many embeddings M</li>
</ol>

We will give examples of the above.  Let's start by generating some pairs:

```sh
$JSALTsrc/C/print_bigrams $scincl/bigrams | sed 1000000q | awk 'rand() < 1/100000' | cut -f2- | head > /tmp/x
cat /tmp/x
# 486	210163984
# 551	8392719
# 2775	164865317
# 3982	7278363
# 4873	147428608
# 5028	167748753
# 7243	95907927
# 7429	144146979
# 7825	119957307
# 8294	38958396
```

<h3 id="pairs2cos">pairs -> cos</h3>

By default, pairs_to_cosine takes no arguments.  It looks up each pair (from stdin) in 5 embeddings:

```sh
$JSALTsrc/pairs_to_cos.sh < /tmp/x
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

```sh
cd $proposed; $JSALTsrc/pairs_to_cos.sh . bins/01* < /tmp/x
.	bins/010	bins/011	bins/012	bins/013	bins/014	bins/015	bins/016	bins/017	bins/018	bins/019
# 0.906	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	551	8392719
# 0.754	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	3982	7278363
# 0.349	-0.022	0.016	0.033	0.026	-0.015	0.009	-0.046	0.034	-0.046	-0.012	8294	38958396
# 0.169	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	7429	144146979
# 0.123	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	4873	147428608
# 0.070	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	7243	95907927
# 0.027	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	2775	164865317
# 0.016	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	7825	119957307
# 0.014	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	486	210163984
# -0.006	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	5028	167748753
```

<h3 id="query2pairs">query -> pairs</h3>

We will use papir 775 as a query.  Since it is a relatively older paper (1979), it will be found in many of the bins.

```sh
echo 775 | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields year,title
# {'paperId': 'b098e9d28f296bcb636e1cc5981393d2ebfab5f3', 'title': 'The blind men and the elephant.', 'year': 1979}
```

The following example shows how to use approximate nearest neighbors (ANN) to find papers
with large cosines in bin 040:

```sh
echo 775 | $JSALTsrc/near_embedding.sh $proposed/bins/040 | head
# 1.000000	775	775
# 0.716708	775	142164003
# 0.700747	775	150176139
# 0.696325	775	180387008
# 0.671397	775	145486868
# 0.662572	775	32720262
# 0.635641	775	149019489
# 0.630416	775	170707795
# 0.612714	775	153169463
# 0.600752	775	60487419
```

The output from above can be piped into other tools such as the semantic scholar API:

```sh
echo 775 | $JSALTsrc/near_embedding.sh $proposed/bins/040 | head | cut -f3 | 
$JSALTsrc/fetch_from_semantic_scholar_api.py --fields year,title
# {'paperId': 'b098e9d28f296bcb636e1cc5981393d2ebfab5f3', 'title': 'The blind men and the elephant.', 'year': 1979}
# {'paperId': '135f8c746eb1c515eda3db8917d06e15b48149be', 'title': 'Learning tomorrows : commentaries on the future of education', 'year': 1979}
# {'paperId': '78240426a71cd5096845480a27a3cae92460259c', 'title': 'In Defense of History', 'year': 1963}
# {'paperId': '5bcbc39f51ba4f5899752b2de1cbb2c91f39b372', 'title': 'Qué es la interdisciplinariedad', 'year': 1983}
# {'paperId': 'd0743f718b99154ed381d19a0c1778329201d533', 'title': 'Coping with Science', 'year': 2019}
# {'paperId': 'a6815c5006aba27cf712298184cde7e6d104c8dc', 'title': 'Learning from experience.', 'year': 1987}
# {'paperId': '1e85d36fed3113f7e5c63317496fa9033b3b6647', 'title': 'Knowledge and Human Interests', 'year': 1973}
# {'paperId': '92736aafeefb74d224879206b5573637918c97be', 'title': 'Heidegger, Education, and Modernity', 'year': 2002}
# {'paperId': '691924dbfe90eb5d0519bec589d88b39ffa21b6f', 'title': 'Anticipatory democracy: People in the politics of the future', 'year': 1978}
# {'paperId': '430fcecca39036d0027c517fda84d06b81fb02e2', 'title': 'Explaining the it gender gap: australian stories', 'year': 2000}
```

The output from above can also be piped into other tools such as pairs to cos:

```sh
cd $proposed; echo 775 | $JSALTsrc/near_embedding.sh $proposed/bins/040 | head | 
cut -f2- | $JSALTsrc/pairs_to_cos.sh . bins/01?
# .	bins/010	bins/011	bins/012	bins/013	bins/014	bins/015	bins/016	bins/017	bins/018	bins/019
# 1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	1.000	775	775
# 0.555	1.000	1.000	0.107	0.040	0.025	0.015	0.102	0.046	0.169	0.200	775	170707795
# 0.555	0.012	0.004	-0.030	0.047	0.096	0.115	0.098	0.167	0.094	0.107	775	150176139
# 0.544	1.000	0.203	-0.013	0.104	0.074	0.108	0.138	0.088	0.133	0.110	775	142164003
# 0.502	1.000	0.089	-0.041	0.069	0.059	0.068	0.176	0.151	0.135	0.088	775	153169463
# 0.492	1.000	1.000	0.107	0.040	0.025	0.015	0.102	0.046	0.169	0.200	775	145486868
# 0.463	1.000	1.000	0.107	0.040	0.025	0.015	0.102	0.046	0.169	0.200	775	32720262
# 0.452	1.000	1.000	0.107	0.040	0.025	0.015	0.102	0.046	0.169	0.200	775	180387008
# 0.408	0.075	0.056	-0.017	0.051	0.037	0.046	0.143	0.206	0.131	0.103	775	149019489
# 0.222	1.000	1.000	0.107	0.040	0.025	0.015	0.102	0.046	0.169	0.200	775	60487419
```

<h3 id="ids2vectors">ids -> vectors</h3>

```sh
cut -f1 < /tmp/x | $JSALTsrc/C/id_to_floats --dir $proposed | cut -f1-10 -d ' '
# 486 405 -0.020542 -0.000371 0.132880 -0.098336 0.134456 -0.074189 -0.018504 0.178263
# 551 461 -0.022954 -0.016283 0.094592 -0.170520 0.124349 -0.071834 0.036887 0.213464
# 2775 2417 -0.012220 -0.063915 0.047094 -0.034431 -0.066762 -0.014799 0.087196 -0.021719
# 3982 3430 -0.016430 -0.015789 0.108481 -0.217662 0.171496 -0.112006 -0.005914 0.221271
# 4873 4177 -0.001826 -0.005093 0.059000 0.024438 0.017045 -0.010485 0.020006 0.045491
# 5028 4310 0.000764 0.003405 0.059788 0.061284 0.018717 -0.024529 -0.030562 0.005923
# 7243 6184 -0.025133 -0.130769 0.080220 -0.000536 -0.152592 0.000375 0.172316 -0.009524
# 7429 6337 -0.023150 -0.017246 0.301845 0.003356 0.181941 -0.167148 -0.094069 0.122514
# 7825 6656 -0.048190 -0.088576 0.165452 -0.176609 -0.000488 -0.098500 0.176909 -0.215839
# 8294 7049 -0.016500 -0.076627 0.133918 -0.081429 -0.109656 0.006693 0.167753 -0.024167
```

<i><b>Warning</b></i>: If a vector is not found in the precomputed embedding, then the second column will be 0,
and the remaining values are not well defined.  We should fix this.

```sh
cut -f1 < /tmp/x | $JSALTsrc/C/id_to_floats --dir $proposed/bins/000 | cut -f1-10 -d ' '
# 486 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 551 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 2775 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 3982 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 4873 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 5028 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 7243 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 7429 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 7825 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
# 8294 0 0.000045 0.000044 0.000202 0.001603 0.000332 0.009979 0.014818 0.002811
```

<h3 id="vector2pairs">vector -> pairs</h3>

The first step is to construct some vectors.  Most of these steps are straightforward,
but x_to_y is a generic tool for converting between types.  With the arg, af, this converts
between ascii (a) and 4-byte floats (f).

```sh
cut -f1 < /tmp/x | $JSALTsrc/C/id_to_floats --dir $proposed | cut -f3- -d ' ' | 
tr ' ' '\n' | $JSALTsrc/C/x_to_y af > /tmp/x.vec
```

The code above input 10 vectors from /tmp/x (in ascii) and output 10 vectors to /tmp/x.vec (in binary).

```sh
wc /tmp/x /tmp/x.vec
   # 10    20   142 /tmp/x
   # 30   193 11200 /tmp/x.vec
   # 40   213 11342 total
```

We can convert them back to ascii and verify that there are 10 vectors with K=280 floats

```sh
$JSALTsrc/C/x_to_y fa < /tmp/x.vec | wc
#   2800    2800   26588
```

The following looks up the 10 inputs vectors and finds the documents that we started with:

```sh
cd $proposed
$JSALTsrc/C/vector_near_with_floats --offset 5 --dir $proposed idx.2?.i  < /tmp/x.vec | sort -u | sort -nr | sed 50q | head
# 1.000000	8294
# 1.000000	7825
# 1.000000	7429
# 1.000000	7243
# 1.000000	551
# 1.000000	5028
# 1.000000	4873
# 1.000000	486
# 1.000000	3982
# 1.000000	2775
```

It also finds many more documents with large cosines:

```sh
cd $proposed
$JSALTsrc/C/vector_near_with_floats --offset 5 --dir $proposed idx.2?.i  < /tmp/x.vec | sort -u | sort -nr | sed 50q | tail
# 0.991628	12182858
# 0.991523	61951604
# 0.991384	5704541
# 0.991326	8564476
# 0.991258	36936139
# 0.991059	5982389
# 0.991007	9433097
# 0.990995	36856498
# 0.990655	44327944
# 0.990294	10254891
```

Note that the examples above used indexes matching idx.2?.i.  There are many more indexes in that directory:

```sh
ls $proposed/idx*.i | wc
     90      90    6570
```

Using more indexes will propose more candidates (and better results), but will take more time.

<h3 id="materialized">Materialized Similarities</h3>

As mentioned above, a number of directories also have some other useful files:
<ol>
<li>proposed/bins/*/*new_pairs: text files with pairs of corpus ids and cosine scores</li>
<li>bigrams: similar to above, but binary files, sorted (without dups) </li>
</ol>


```sh
sed 100000q $proposed/bins/000/idx.19.i.new_pairs | awk '$1 < 1' | sort -nr | head 
# 0.999999	9176071	27917253
# 0.999999	9176071	19184716
# 0.999999	4821225	19184716
# 0.999999	4290997	9176071
# 0.999999	4290997	4821225
# 0.999999	4290997	18324989
# 0.999999	4290997	18229117
# 0.999999	4290997	10163138
# 0.999999	3949462	9176071
# 0.999999	3949462	4821225
```

```sh
$JSALTsrc/C/print_bigrams < $proposed/bigrams | head
# 0.93	2	1882
# 0.92	2	73308
# 0.92	2	96619
# 0.87	2	106894
# 0.93	2	115452
# 0.91	2	159197
# 0.92	2	199806
# 0.90	2	220406
# 0.94	2	256488
# 0.94	2	282449
```

See <a href="materialized_similarities.md">here</a> for more discussion of materialized similarities.
