# Time partitioning

There are about 200M corpusIds.
<p>
Each of these is assigned a timestamp (based on publication date).
We split the 200M ids into 100 files of about 2M ids each.
<p>
The 100 file names are $JSALTdir/semantic_scholar/j.ortega/graphs.V2/0[0-9][0-9].
<p>
The following outputs the first id in 10 files.  We then pull the year
to show that the 10 files are partitioned by time.  Since the
literature is growing exponentially, the gaps between years is
becoming smaller and smaller in more recent years.

```sh
for f in $JSALTdir/semantic_scholar/j.ortega/graphs.V2/0[0-9]0
do
sed 1q $f
done | 
$JSALTsrc/fetch_from_semantic_scholar_api.py --fields year
# {'paperId': '4a183ff2cbf6ab7299b060be49e134c299632f68', 'year': 1896}
# {'paperId': 'ecbc1196073ee62ff51d59015b2dc32b72397487', 'year': 1980}
# {'paperId': '3f1a6cabc60a1250ece2861fc6fabddb4199f485', 'year': 1994}
# {'paperId': '71a5309dc40fdd8b48af26ff3da903c4d25b255c', 'year': 2002}
# {'paperId': '38591ed1430d14479a361006ba57fb52301d0965', 'year': 2006}
# {'paperId': 'b74053d245a17283f3fec43a5996f1cdebfd93f2', 'year': 2010}
# {'paperId': 'ab574e2dedccd3acb9a8a4cb30f6b18fa3ffb73a', 'year': 2013}
# {'paperId': '1d8e9c65519611c206ddd060e49d155ec85030f3', 'year': 2015}
# {'paperId': '1161b928bb112dd15135711e938258d27f182988', 'year': 2018}
# {'paperId': '00b0452cc6cefc7a288042c5979fcc60b71c1e58', 'year': 2020}
```

<h2>Sparse Graphs</h2>

You can load these with: <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.save_npz.html">scipy.sparse.load_npz</a>
<p>
There are 100 graphs in graphs.V2 and 100 in cumgraphs.V2.
<p>
graphs.V2 is filtered, so 000.npz has edges leaving the 2M ids in 000.
<p>
These graphs become larger over time, becasue these edges can terminate on ids that predate
the citing paper.
<p>
Cumgraphs contain the sum of all graphs before them.  These files grow more quickly, as one might expect.

```sh
du -h $JSALTdir/semantic_scholar/j.ortega/graphs.V2/0[0-9]0.npz
# 4.9M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/000.npz
# 32M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/010.npz
# 45M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/020.npz
# 59M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/030.npz
# 67M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/040.npz
# 77M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/050.npz
# 91M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/060.npz
# 96M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/070.npz
# 105M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/080.npz
# 139M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/graphs.V2/090.npz
```

```sh
du -h $JSALTdir/semantic_scholar/j.ortega/cumgraphs.V2/0[0-9]0.npz
# 4.9M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/000.npz
# 196M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/010.npz
# 583M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/020.npz
# 1.1G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/030.npz
# 1.7G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/040.npz
# 2.4G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/050.npz
# 3.2G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/060.npz
# 4.1G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/070.npz
# 5.1G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/080.npz
# 6.2G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/090.npz
```

These are symmetric (undirected) versions of the above.  That is, M = M + M.T

```sh
du -h $JSALTdir/semantic_scholar/j.ortega/cumgraphs.V2/0[0-9]0.sym.npz
# 8.9M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/000.sym.npz
# 389M	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/010.sym.npz
# 1.2G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/020.sym.npz
# 2.2G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/030.sym.npz
# 3.4G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/040.sym.npz
# 4.8G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/050.sym.npz
# 6.4G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/060.sym.npz
# 9.0G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/070.sym.npz
# 12G	/work/k.church/JSALT-2023//semantic_scholar/j.ortega/cumgraphs.V2/080.sym.npz
```

I am currently running ProNE on these graphs.  See
/scratch/k.church/JSALT-2023/semantic_scholar/j.ortega/cumgraphs.V2
for partial results.

