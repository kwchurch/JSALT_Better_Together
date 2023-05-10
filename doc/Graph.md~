# Example of a Graph


Graphs are stored as N by N sparse matrics, with E edges.  N is set to
be large enough to hold Semantic Scholar corpusIds, with some room for
expansion.  Note, many rows and cols have no counts, because those
corpusIds do not appear in the graph.

```python
import scipy.sparse
f='/work/k.church/JSALT-2023/semantic_scholar/releases/2022-12-02/database/citations/graphs/citations.G.npz'

# Note: this is very slow.
G=scipy.sparse.load_npz(f)

G.shape
# (270000000, 270000000)
G.dtype
dtype('bool')

G.count_nonzero()/1e9
# 2.148022917

# The file is less than 10 GBs on disk,
# but expands to about 20 GBs when loaded into python.
(G.data.nbytes , G.indices.nbytes , G.indptr.nbytes)/1e9
# 21.492206261
```