# load sparse matrices quickly

scipy.sparse.save_npz and scipy.sparse.load_npz are slow (and use a lot of space).
<p>
There are some faster alternatives in $JSALTsrc/JSALT_util.py
<p>
Here is an example for a big sparse matrix (papers_to_authors).  This
example assumes the current working directory
is $JSALTdir/semantic_scholar/releases/2023-06-20/database/papers

Here is the slow way:
```python
import numpy as np
import scipy
M=scipy.sparse.load_npz('papers_to_authors.npz')
```

Here is the faster way, where my_load_csr_matrix is defined
in $JSALTsrc/JSALT_util.py

```python
M2 = my_load_csr_matrix('papers_to_authors')
```
