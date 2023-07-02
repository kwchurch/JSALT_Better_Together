# What's Where

<h2>Globus: Big Files</h2>

For those of you with access to Northeastern Cluster:

```sh
JSALTdir=/work/k.church/JSALT-2023/
```

These files are reachable from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2F">Globus</a>



<h3>Embeddings</h3>

There is a README file <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Fembeddings%2F">here</a>.

<ol>
<li>embeddings/proposed: $proposed</li>
<li>embeddings/scincl: $scincl</li>
<li>embeddings/specter2</li>
<li>embeddings/specter.K280</li>
<li>embeddings/specter: $specter</li>
<li>embeddings/LinkBERT</li>
</ol>

There is a machine readable file here: embeddings/all_embeddings.txt;
You can find mentions to this file under $JSALTsrc/*.sh
<p>
The proposed method is based on citation graphs and ProNE.
<p>
Specter is based on embeddings from the bulk download.  These are probably the same as
the ad hoc API, but not the same as models on huggingface.
<p>
Specter2 is based on <a href="https://huggingface.co/allenai/specter2">this model</a>.
We ran that on many files with abstracts that we could download from the bulk download.
There are more papers with embeddings than abstracts (because some abstracts cannot be distributed).
<p>
specter.K280 is a smaller version of specter (K=768).  I used random projections to reduce K from 768 to 280.
<p>
We are still computing production runs on LinkBERT.  That should be ready soon, but LinkBERT is probably not as good as the others.
<p>
There will soon be some large files in $scincl/bigrams, $proposed/bigrams, $specter/bigrams.
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
 
<h3>Releases</h3>

See releases/README.txt and <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/doc/bulk_download/semantic_scholar_bulk_download.md">documentation on bulk downloading from Semantic Scholar</a>.

<ol>
<li>releases/2022-12-02</li>
<li>releases/2023-05-09</li>
<li>releases/2023-06-20</li>
</ol>

<h2>Citing Sentences</h2>

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

<h2>Citation Graphs</h2>

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

<h2>Mapping Papers to Authors</h2>

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

