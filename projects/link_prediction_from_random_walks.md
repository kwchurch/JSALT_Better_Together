# Suggestion for project: link prediction from random walks

See <a href="https://github.com/kwchurch/JSALT_Better_Together/tree/main/doc/measurements/ProNE.20230723">here</a> for some background material

I started with $JSALTdir/semantic_scholar/eval/walk_with_bins

```sh
# head $JSALTdir/semantic_scholar/eval/walk_with_bins
# dist	id1	id2	bin1	bin2
# 1	248518397	1041744	97	51
# 2	248518397	23848439	97	21
# 3	248518397	4235810	97	12
# 4	248518397	82079949	97	11
# 1	3374228	140728989	79	0
# 1	68334187	36144275	58	34
# 2	68334187	7008060	58	4
# 1	205881482	94036919	77	72
# 2	205881482	95069173	77	53
```

id1 and id2 are corpus ids
<p>
dist should be the distance from id1 to id2 (please check me on that)
<p>
The link prediction task is to predict if dist is 1 or not.
<p>
I'd like to train on some bins and test on some others.  I'd expect performance to depend on bin1 and bin2.
The task should be easier when both bins are in the training set, and hardest when both bins are far from the taining set.
<p>
There are many files like these.  I split walk_with_bins into pieces walk12.??.  For each pair in each piece,
we have a cosine and a pair of corpus ids.  The corpus ids should match walk_with_bins.
<p>
<b>NOTE</b>: A cosine of -1 should be interpreted as NA (not available).
<p>
The pathname encodes the model (scincl), as well as the value of use_references.  As explained <a href="https://github.com/kwchurch/JSALT_Better_Together/tree/main/doc/measurements/ProNE.20230723">here</a>, use_references can be (a) always, (b) never, or (c) when_necessary.  

```sh
head $scincl/walk_pieces/*/walk12.aa
==> /work/k.church/JSALT-2023//semantic_scholar/embeddings/scincl/walk_pieces/always/walk12.aa <==
0.9758153	248518397	1041744
0.8967998	248518397	23848439
0.8941157	248518397	4235810
-1	248518397	82079949
-1	3374228	140728989
0.9322941	68334187	36144275
-1	68334187	7008060
0.95059776	205881482	94036919
0.8640236	205881482	95069173
0.8887665	205881482	53480264

==> /work/k.church/JSALT-2023//semantic_scholar/embeddings/scincl/walk_pieces/never/walk12.aa <==
-1	248518397	1041744
-1	248518397	23848439
-1	248518397	4235810
-1	248518397	82079949
0.86788625	3374228	140728989
0.8860135	68334187	36144275
-1	68334187	7008060
-1	205881482	94036919
-1	205881482	95069173
-1	205881482	53480264

==> /work/k.church/JSALT-2023//semantic_scholar/embeddings/scincl/walk_pieces/when_necessary/walk12.aa <==
0.9236629	248518397	1041744
0.8189676	248518397	23848439
0.82118046	248518397	4235810
-1	248518397	82079949
0.86788625	3374228	140728989
0.8860135	68334187	36144275
-1	68334187	7008060
0.95059776	205881482	94036919
0.8640236	205881482	95069173
0.82201785	205881482	53480264
```
<p>
There are 882 files like this:

```sh
find /work/k.church/JSALT-2023/semantic_scholar/embeddings/ -name 'walk12.??'  | wc
#    882     882   90027
```

Most of the 882 files are under bins

```sh
find /work/k.church/JSALT-2023/semantic_scholar/embeddings/ -name 'walk12.??' | egrep -c bins
756
```

I used those files to compute the coverage tables <a href="https://github.com/kwchurch/JSALT_Better_Together/tree/main/doc/measurements/ProNE.20230723">here</a>.
<p>
It would be very interesting to combine those results with the ones below.  These show cosines for standard embeddings with (and without)
the centroid assumption.  I would like to see a better togther story where adding embeddings based on text improves coverage and predictions, especially
far into the future.
<p>
Note: to save space, I am only showing walk12.aa, but there are also files matching walk12.[a-z][a-z]

```sh
find /work/k.church/JSALT-2023/semantic_scholar/embeddings/ -name 'walk12.aa' | egrep -v bins
/work/k.church/JSALT-2023/semantic_scholar/embeddings/LinkBERT/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/LinkBERT/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/LinkBERT/walk_pieces/when_necessary/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/proposed/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/proposed/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/proposed/walk_pieces/when_necessary/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/scincl/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/scincl/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/scincl/walk_pieces/when_necessary/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter/walk_pieces/when_necessary/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter.K280/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter.K280/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter.K280/walk_pieces/when_necessary/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter2/walk_pieces/always/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter2/walk_pieces/never/walk12.aa
/work/k.church/JSALT-2023/semantic_scholar/embeddings/specter2/walk_pieces/when_necessary/walk12.aa
```
