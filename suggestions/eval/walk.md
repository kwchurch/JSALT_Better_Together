# Suggestions for random walks

See walk file under <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Feval%2F">here</a>.

<p>
There are 3.5M rows like this:

```sh
head walk
# 1	248518397	1041744
# 2	248518397	23848439
# 3	248518397	4235810
# 4	248518397	82079949
# 1	3374228	140728989
# 1	68334187	36144275
# 2	68334187	7008060
# 1	205881482	94036919
# 2	205881482	95069173
# 3	205881482	53480264
```

We started with a random query (column 2) and then walked to one of
its references (column 3) randomly.  From there, we continued until we
couldn't go any more.
<p>
Column 1 is distance from column 2 to column 3.
<p>
The combo.V3 file under <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Feval%2Fresults%2Fwalk%2F">here</a> contains the information above, as well as cosine scores for many systems.

<ol>
<li><ol>methods
<li> proposed, proposed.out</li>
<li> proposed method based on bins: 
bins/000.out,
bins/001.out,
bins/005.out,
bins/010.out,
bins/015.out,
bins/018.out,
bins/019.out</li>
<li> like above, but using code from nodevectors (as opposed to our rewrite):
bins/prone.baseline/000.out,
bins/prone.baseline/001.out,
bins/prone.baseline/005.out</li>
<li> scincl, scincl.out </li>
<li> specter2, specter2.out </li>
<li> specter, specter.out</li>
<li>specter.K280, specter.K280.out: like above, but downsampled from K=768 to K=280, using random projections </li>
<li> LinkBERT.out </li>

</ol></li>
<li>dist: a number between 1 and 4</li>
<li> ids: corpusId1, corpusId2, id1, id2</li>
</ol>

<img src="combo.V3.jpg" alt="Clustering of Above" width="1000" />


