# What's Where: Big Files on Globus

<h2>Globus: Big Files</h2>

We are distributing many large files via <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2F">Globus</a>.

For those of you with access to Northeastern Cluster, these files can be found
under $JSALTdir.  We will use the following environment variables.


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


<p>
There is a quota of 35T (terabytes) on /work/k.church.  There is no quota on /scratch, but files
are deleted after about 30 days, and we are not sharing those files on Globus.


<h3>Overview</h3>

<ol>
<li><a href="#Embeddings">Embeddings</a></li>
<li><a href="#bigrams">Bigrams (pairs of corpusIds with large cosines)</a></li>
<li><a href="#Releases">Releases (Bulk Downloads from Semantic Scholar)</a></li>
<li><a href="#CitingSentences">Citing Sentences</a></li>
<li><a href="#CitationGraphs">Citation Graphs</a></li>
<li><a href="#authors">Papers to Authors</a></li>
<li><a href="#venues">Papers to Venues</a></li>
</ol>


<h3 id="Embeddings">Embeddings</h3>

There is a README file <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Fembeddings%2F">here</a>.

<ol>
<li>embeddings/proposed: $proposed</li>
<li>embeddings/scincl: $scincl</li>
<li>embeddings/specter2: $specter2</li>
<li>embeddings/specter: $specter</li>
<li>embeddings/specter.K280 (same as above, but used random projections to reduce K from 768 to 280)</li>
<li>embeddings/LinkBERT: $LinkBERT</li>
</ol>

There is a machine readable file here: embeddings/all_embeddings.txt;
You can find mentions to this file under $JSALTsrc/*.sh
<p>
The proposed method is based on citation graphs and ProNE.
<p>
Specter is based on embeddings from the <a href="https://api.semanticscholar.org/api-docs/datasets">bulk download API</a>.
These are probably the same as
the <a href="https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_get_paper">ad hoc API</a>,
but not the same as the <a href="https://huggingface.co/allenai/specter">specter model on huggingface</a>.
<p>
Specter2 is based on <a href="https://huggingface.co/allenai/specter2">this model</a>.
We ran that on many files with abstracts that we could download from the bulk download.
There are more papers with embeddings than abstracts (because some abstracts cannot be distributed).
<p>
specter.K280 is a smaller version of specter (K=768).  I used <a
href="https://hastie.su.domains/Papers/Ping/KDD06_rp.pdf">random
projections</a> to reduce K from 768 to 280.
<p>
<a href="https://huggingface.co/michiyasunaga/LinkBERT-large">LinkBERT</a> is probably not as good as the others.

<h3 id="bigrams">Bigrams</h3>

There are some large files in 
<ol>
<li>$JSALTdir/semantic_scholar/embeddings/proposed/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/scincl/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/specter/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/specter2/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/LinkBERT/bigrams</li>
</ol>
These are materialized files with the large values from: M @ M.T.  There are N^2 values in M@M.T,
but only N values in each index.  The materialized files are based on those.
<p>
We can query bigrams with this:

```sh
query=3051291
echo $query |
$JSALTsrc/C/x_to_y ai | 
$JSALTsrc/C/extract_row $scincl/bigrams |
$JSALTsrc/C/print_bigrams | 
sort -nr |
 head | 
cut -f3 | 
$JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/papers/corpusId_to_href
```
We can score bigrams by a number of embeddings with this:

```sh
echo 3051291 | 
$JSALTsrc/C/x_to_y ai | 
$JSALTsrc/C/extract_row $scincl/bigrams | 
$JSALTsrc/C/print_bigrams | 
sort -nr |
sed 3q |
cut -f2- |
$JSALTsrc/pairs_to_cos.sh |
$JSALTsrc/tsv_to_html.sh
 ```

Here is the output from the above:

<html><table><tr>
<th>proposed</th>
<th>scincl</th>
<th>specter2</th>
<th>specter</th>
<th>specter.K280</th>
</tr>
<tr>
<td>0.947</td>
<td>0.951</td>
<td>0.970</td>
<td>0.797</td>
<td>0.792</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">7513: DeepWalk: online learning of social representations</a></td>
<td><a href="https://www.semanticscholar.org/paper/e294339b402ce055d5a5198becc35b2dbbd20a9a">5: SimWalk: Learning network latent representations with social relation similarity</a></td>
</tr>
<tr>
<td>0.827</td>
<td>0.997</td>
<td>0.999</td>
<td>0.984</td>
<td>0.983</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">7513: DeepWalk: online learning of social representations</a></td>
<td><a href="https://www.semanticscholar.org/paper/93b050f5bf0567a675979cd564cbe66ff9c3a78f">0: Learning of Social Representations</a></td>
</tr>
<tr>
<td>0.704</td>
<td>0.932</td>
<td>0.960</td>
<td>-1.000</td>
<td>-1.000</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">7513: DeepWalk: online learning of social representations</a></td>
<td><a href="https://www.semanticscholar.org/paper/0abbe9e3eee8649e2588f8db6ad500c6d60f8990">1: Learning representations on graphs</a></td>
</tr>
</table></html>
 
<h3 id="Releases">Releases (Bulk Downloads from Semantic Scholar)</h3>

See releases/README.txt and <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/doc/bulk_download/semantic_scholar_bulk_download.md">documentation on bulk downloading from Semantic Scholar</a>.

<ol>
<li>releases/2022-12-02</li>
<li>releases/2023-05-09</li>
<li>releases/2023-06-20</li>
</ol>

<h3 id="CitingSentences">Citing Sentences</h3>

The big files are here: <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2022-12-02%2Fdatabase%2Fcitations%2Fciting_sentences%2F">$JSALTdir/semantic_scholar/releases/2022-12-02/database/citations/citing_sentences</a>.
<p>
<ol>
<li>embedding: *.f (4 TB file), with indexes (idx*i)</li>
<li>embedding.K280: same as above, but used random projections to make the file smaller (by reducing K from 768 to 280) </li>
<li>pieces: text files behind the above</li>
</ol>

The citing sentences can be extracted from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2023-06-20%2Fdatabase%2Fcitations%2F">bulk downloads</a>, as well as ad hoc queries.
<p>
For documentation on ad hoc query, see discussion of citing sentences in these <a href="https://github.com/kwchurch/JSALT_Better_Together/tree/main/doc/exercises">exercises</a>.

<h3 id="CitationGraphs">Citation Graphs</h3>

There is an npz file <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2022-12-02%2Fdatabase%2Fcitations%2Fgraphs%2F">here</a>
<p>
The following loads a npz file into python:

```python
import numpy as np
import scipy
f='citations.G.npz'
M=scipy.sparse.load_npz(f)
```

M is a boolean matrix, a graph in adjacency format.  There is a 1 in M[i,j] iff paper i cites paper j.
<p>
There are many more graphs <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Fj.ortega%2Fcumgraphs.V2%2F">here</a>
<p>
Files with 3-digit names ([0-9][0-9][0-9]) are lists of corpusids.
There are nearly 100 such files.  Each file contains approximating the
same number of ids, partitioned by publication date.
<p>
These files ([0-9][0-9][0-9].sym.npz) are boolean matrices.  The keyword sym means
that the matrix is undirected (M = M + M.T).  001.sym.npz contains edges that start with corpusids in 001.
<p>
The point of splitting corpusids in this way is described <a
href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/suggestions/eval/cite.md">here</a>.
If we train on papers from one point in time and test on another,
we expect to be more successful with predictions into the near future than into the distant future.

<h4>Years</h4>

There are 100 files of the form [0-9][0-9][0-9].years.txt.  These
files have a pair of years and a count of citations.  The first column has
the publication year of the paper, and the second column has the publication year of the reference.
Normally, the first column is after the second, but not always.

```sh
egrep '^2010' $JSALTdir/semantic_scholar/j.ortega/cumgraphs.V2/050.years.txt | sort -nr -k3 | head
# 2010 2007 2244265
# 2010 2008 2214234
# 2010 2006 2118897
# 2010 2005 1972017
# 2010 2004 1850326
# 2010 2009 1663334
# 2010 2003 1636488
# 2010 2002 1475746
# 2010 2001 1337063
# 2010 2000 1243128
```

One would hope that citations are causal.  We see more citations in the expected direction than vice versa, but both directions are possible.

```sh
cd $JSALTdir/semantic_scholar/j.ortega/cumgraphs.V2
awk '{delta = $1 - $2; 
      if(delta < -10) delta=-10; 
      if(delta > 10) delta=10; x[delta]+= $3}; 
  END {for(i in x) print x[i], i }' 000.years.txt | sort -nr
# 416734 10
# 101396 1
# 83798 2
# 81178 -1
# 64643 3
# 51628 4
# 51543 0
# 40782 5
# 33575 6
# 28794 7
# 24846 8
# 21401 9
# 1204 -2
# 234 -3
# 204 -4
# 184 -8
# 175 -7
# 171 -6
# 169 -5
# 137 -10
# 131 -9
```

<h3 id="authors">Mapping Papers to Authors</h3>

See <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2023-06-20%2Fdatabase%2Fpapers%2Fauthors%2F">here</a>.
<p>

You can load that matrix with this:

```python
f='papers_to_authors.npz'
import numpy as np
import scipy
M=scipy.sparse.load_npz(f)
M.shape
# (259187462, 2220213919)
M[3051291,:].nonzero()
# (array([0, 0, 0]), array([   1721948,    2271808, 1388360943]))
```

This says that paper <a href="https://www.semanticscholar.org/paper/DeepWalk%3A-online-learning-of-social-representations-Perozzi-Al-Rfou/fff114cbba4f3ba900f33da574283e3de7f26c83">3051291</a> has three authors:
<a href="https://www.semanticscholar.org/author/Bryan-Perozzi/1721948">1721948</a>,
<a href="https://www.semanticscholar.org/author/Bryan-Perozzi/2271808">2271808</a>
and
<a href="https://www.semanticscholar.org/author/Bryan-Perozzi/1388360943">1388360943</a>.

If you want to combine that matrix with an N by N matrix, G, you can say something like this:

```python
M.resize(270000000, 2220213919)
G @ M.T
```


```python
f='/work/k.church/JSALT-2023/semantic_scholar/embeddings/proposed/bigrams.npz'
import numpy as np
import scipy
bigrams=scipy.sparse.load_npz(f)
```

<h3 id="venues">Mapping Papers to Venues</h3>

See <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2023-06-20%2Fdatabase%2Fpapers%2Fvenues%2F">here</a>.

<p>
There are about 300k venues in this file

```sh
head $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/venues/venue.key
# 1	00001b09686f837ed973f5a617757eae	Hacking Diversity
# 2	00007856c258f947325ed50fa8052710	Indian journal of medical education
# 3	0000e5f17837d8ffc403e9c0542feee9	TheStrategy Factor in Successful Language Learning
# 4	0000f96e5a7f80b27c68273404a1c413	Derecho Público Iberoamericano
# 5	000109714dc88a5c27ad3346f3959c05	Pedagogical Review
# 6	00012785e8018ed2cf0646fa301134e5	Barbey d'Aurevilly : «L'ensorcelée»
# 7	00019dd47d09d5867b466e56bb9c09fb	Doing Space while Doing Gender - Vernetzungen von Raum und Geschlecht in Forschung und Politik
# 8	0001aed83bdb255857a2a4acadc9412b	Ceddi Journal of Education
# 9	0001cbe48f6594391bb9a190db2f19fc	Stuck and Exploited  Refugees and Asylum Seekers in Italy Between Exclusion, Discrimination and Struggles
# 10	0001f58abbed5b3ffd5e30b39e41e076	JURNAL TEOLOGI GRACIA DEO
```

find_lines looks up ids in the input file
<p>
corpusId_to_href is a text file that maps between Semantic Scholar corpusId and href (html string)
<p>
The href contains a URL to Semantic Scholar for the appropriate paper
<p>

```sh
echo 3051291 | $JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/href/corpusId_to_href
# 3051291	<a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">5853: DeepWalk: online learning of social representations</a>
```

Similar to above, but maps corpusIds to venues:

```sh
echo 3051291 | $JSALTsrc/C/find_lines --input $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/venues/corpusId_to_venue
# 3051291	2014	Knowledge Discovery and Data Mining
```


col1 is venue id

```sh
egrep 'Computational Ling' venue.key | head | cut -f1 | find_lines --input venue.key
# 6288	0451aa778b60ee723311e6ea72695259	Proceedings of the Workshop on Human Judgements in Computational Linguistics - HumanJudge '08
# 10373	071abff3a8f40e6bda81d0c870f25c68	International Conference on Computational Linguistics
# 13102	09066ac80cc0675de0a2fb6471f73fc3	Proceedings of the conference. Association for Computational Linguistics. North American Chapter. Meeting
# 27101	1294418a3a196689abe17609b96b673c	Italian Conference on Computational Linguistics
# 34421	17919bf36f434566dd4c3864edf28b2c	ACL Microfiche Series 1-83, Including Computational Linguistics
# 49168	21ae9b7793088db42057adc0447bef9a	Recent Topics in Mathematical and Computational Linguistics
# 61416	2a1b9d121a6e409bf90c38866d975548	Sanskrit Computational Linguistics
# 77577	350d302be588f5f80d36e9fcfe0cfd1d	Proceedings of the Seventh Italian Conference on Computational Linguistics CLiC-it 2020
# 87493	3bede9261108e7b91b03de5df243e7cb	Workshop on Cognitive Modeling and Computational Linguistics
# 89677	3d76be9880fbc2806af4f5870788ff2d	Conference Of The European Association For Computational Linguistics
```

Suggestion: join this file with bigrams:

<ol>
<li>$JSALTdir/semantic_scholar/embeddings/proposed/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/scincl/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/specter/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/specter2/bigrams</li>
<li>$JSALTdir/semantic_scholar/embeddings/LinkBERT/bigrams</li>
</ol>

