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

There is an npz file <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2022-12-02%2Fdatabase%2Fcitations%2Fgraphs%2F>here</a>
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
There are many more graphs <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Fj.ortega%2Fcumgraphs%2F">here</a>
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
