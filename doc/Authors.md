# How to map between papers and authors and vice versa

We will be referring to these files on Globus: <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2023-06-20%2Fdatabase%2Fpapers%2Fauthors%2F">here<a>.

If you has access to the Northeastern cluster, these files are here:

```sh
export JSALTdir=/work/k.church/JSALT-2023/
cd $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/authors
```

<b>NOTE</b>: The following resources are based on a release from a few months ago.  If you compare results
from these resources with the online version of Semantic Scholar, you will find some differences, largely due to
recent publications.
<p>
<h2>Simple</h2>
The simplest way to use these files is this:

```python
import numpy as np
import scipy
f='papers_to_authors.npz'
M=scipy.sparse.load_npz(f)
```

M is a sparse boolean matrix, with a 1 in M[i,j] iff paper i was written by paper j.

```python
M.shape
# (259187462, 2220213919)
M.dtype
# dtype('bool')
```

There are nearly 600M nonzero values in M.  Since there are about 200M papers in Semantic Scholar, this
means there are about 3 authors for each paper, on average.

```python
M.count_nonzero()
# 592995277
M.count_nonzero()/1e6
592.995277
```

Note: many of the rows and columns are empty because there are many gaps in Semantic Scholar CorpusIds and authorIds.
CorpusIds are more dense than authorIds.  There are about 260M CorpusIds in M, slightly more than the number of papers (200M).
There are 2B authorIds, but most of them have no papers.  That is, most of the columns in M are empty.

<p>
Suppose we have a CorpusId, 2, and we want to know who wrote that paper.
The following says that paper has 6 authors:

```python
papers,authors = M[2,:].nonzero()
authors
# array([ 1712216,  1720683,  1738575,  1744439,  1790055, 48280839])
```

There is a simple mapping between authorId and URLs on Semantic Scholar:

<ol>
<li><a href="https://www.semanticscholar.org/author/1712216">https://www.semanticscholar.org/author/1712216</a></li>
<li><a href="https://www.semanticscholar.org/author/1720683">https://www.semanticscholar.org/author/1720683</a></li>
<li><a href="https://www.semanticscholar.org/author/1738575">https://www.semanticscholar.org/author/1738575</a></li>
<li><a href="https://www.semanticscholar.org/author/1744439">https://www.semanticscholar.org/author/1744439</a></li>
<li><a href="https://www.semanticscholar.org/author/1790055">https://www.semanticscholar.org/author/1790055</a></li>
<li><a href="https://www.semanticscholar.org/author/48280839">https://www.semanticscholar.org/author/48280839</a></li>
</ol>

Ditto for CorpusId:

<ol>
<li><a href="https://api.semanticscholar.org/CorpusId:2">https://api.semanticscholar.org/CorpusId:2</a></li>
</ol>

The following finds 209 papers by author 1712216:

```python
papers,authors = M[:,1712216].nonzero()
len(papers)
# 209
papers[0:10]
# array([      2,  237611,  377241,  872899, 1812868, 2079957, 2263609,
#       2363214, 2461856, 2499619], dtype=int32)
```

You can click on the following iinks to verify that they share a common author:

<ol>
<li><a href="https://api.semanticscholar.org/CorpusId:2">https://api.semanticscholar.org/CorpusId:2</a></li>
<li><a href="https://api.semanticscholar.org/CorpusId:237611">https://api.semanticscholar.org/CorpusId:237611</a></li>
<li><a href="https://api.semanticscholar.org/CorpusId:377241">https://api.semanticscholar.org/CorpusId:237611</a></li>
</ol>

Sparse matrices are convenient to work with, though maybe not so fast:
This is basically the same as the above.  You probably want to make sure you
have enough memory to avoid thrashing.

```python
authors,papers = M.T[1712216,:].nonzero()
```

These are super-easy, but again, remarkably slow:

```python
fan0 = M.sum(axis=0) # count of papers by author
fan1 = M.sum(axis=1) # count of authors by papers 
```

This is probably not bad, though I haven't tested this:

```python
bin0 = np.bincount(np.array(fan0[0,:]), dtype=np.int32)
bin1 = np.bincount(np.array(fan1[:,0]), dtype=np.int32)
```

<h2>Faster</h2>

There is a faster alternative to load_npz <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/src/JSALT_util.py">here</a>.
<p>


This code makes use of the .X.i and .Y.i files:

```python
cd $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/authors
echo 2 | $JSALTsrc/extract_row.py -G papers_to_authors --longs_and_doubles
# 2	1712216
# 2	1720683
# 2	1738575
# 2	1744439
# 2	1790055
# 2	48280839
```

The code above uses memory mapping:

```python
def map_int64(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int64, shape=(int(fn_len/8)), mode='r')

def map_int32(fn):
    fn_len = os.path.getsize(fn)
    return np.memmap(fn, dtype=np.int32, shape=(int(fn_len/4)), mode='r')
```

There is a better solution in $JSALTsrc/cluster_authors.py

```python
# Y = my_idx = None
X = map_int64(args.author_to_papers + '.X.i')
Y = map_int64(args.author_to_papers + '.Y.i')

def extract_row(x):
    left = np.searchsorted(X, x, side='left')
    right = np.searchsorted(X, x, side='right')
    return Y[left:right]
```

Since it is expensive to take the transpose of these large matrices, there are files like these:

<ol>
<li>authors_to_papers.X.i</li>
<li>papers_to_authors.X.i</li>
</ol>

The first file maps author ids to paper ids, and the second maps
paper ids to author ids.


<h2>Simple Unix Script to Count Papers by Author</h2>

```sh
export JSALTdir=/work/k.church/JSALT-2023/
cd $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers/authors
$JSALTsrc/C/x_to_y La < authors_to_papers.X.i | uniq -c | awk '$1 > 1000'  | head
   # 1081 1679177
   # 1574 1679424
   # 8143 1679704
   # 1069 1679790
   # 1111 1680165
   # 1522 1681236
   # 2184 1682058
   # 1266 1682342
   # 3941 1682816
   # 1055 1682912
```

Here are some links to those authors:

<ol>
<li><a href="https://www.semanticscholar.org/author/1679177">https://www.semanticscholar.org/author/1679177</a></li>
<li><a href="https://www.semanticscholar.org/author/1679424">https://www.semanticscholar.org/author/1679424</a></li>
<li><a href="https://www.semanticscholar.org/author/1679704">https://www.semanticscholar.org/author/1679704</a></li>
<li><a href="https://www.semanticscholar.org/author/1679790">https://www.semanticscholar.org/author/1679790</a></li>
<li><a href="https://www.semanticscholar.org/author/1680165">https://www.semanticscholar.org/author/1680165</a></li>
<li><a href="https://www.semanticscholar.org/author/1681236">https://www.semanticscholar.org/author/1681236</a></li>
<li><a href="https://www.semanticscholar.org/author/1682058">https://www.semanticscholar.org/author/1682058</a></li>
<li><a href="https://www.semanticscholar.org/author/1682342">https://www.semanticscholar.org/author/1682342</a></li>
<li><a href="https://www.semanticscholar.org/author/1682816">https://www.semanticscholar.org/author/1682816</a></li>
<li><a href="https://www.semanticscholar.org/author/1682912">https://www.semanticscholar.org/author/1682912</a></li>
</ol>

The following will find papers with more than 100 authors:

```sh
$JSALTsrc/C/x_to_y La < papers_to_authors.X.i | uniq -c | awk '$1 > 100' | head
    498 3995
    151 6666
    101 14058
    134 15056
    104 22619
    439 24334
    104 25175
    500 29047
    146 32454
    868 49627
```
