# Better Together Team Github
# JSALT (Jelinek Summer Workshop on Speech and Language Technology): 

<h2>Useful links</h2>
<ol>
<li>Github: https://github.com/kwchurch/JSALT_Better_Together</li>
<li>Slides: included in Github</li>
<li>Team Page: <a href="https://jsalt2023.univ-lemans.fr/en/better-together-text-context.html">Better Together: Text + Context</a></li>
<li>large datasets: <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">Globus</a></li>
<li>Zoom Link: https://northeastern.zoom.us/j/8963791015</li>
<li>Meeting Notes: <a href="https://docs.google.com/document/d/1rRRflCASHo7PFTBU6GqHK_g8twj1JgcXD8ijwpWY9m8/edit">Google Doc</a></li>
</ol>

<h2>Deliverables</h2>
<ol>
<li>Better access to literature</li>
<li>Resources: 
n    <ol>
    <li>Many embeddings for many papers</li>
    <li>More models to be posted on HuggingFace</li>
    <li>Code to be posted on GitHub</li></ol>
</li>
<li>Methods to compare and contrast across small (and large) collections of documents</li>
<li>Support incremental updates to embeddings based on citation graphs</li>
<li>Evaluation: Better numbers, as well as better benchmarks</li>
<li>Establish that combinations of text and links are better together (than either by itself)</li>
<li>Establish that citing sentences are useful</li>
<li>Improve methods for assigning papers to reviewers</li>
<li>Theory: Unified framework of deep nets and Linear Algebra</li>
</ol>

<h2>Installation</h2>

```sh
git clone https://github.com/kwchurch/JSALT_Better_Together
pip install -r requirements.txt
```

Some useful environment variables; you may need to set these up differently, depending on where you put stuff.
JSALTsrc should be assigned to the src directory in this repo.
JSALTdir should be assigned to the data from <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">Globus</a>.

Some examples below depend on JSALTdir and some do not.  If you cannot download JSALTdir, try the examples that do not require that.

```sh
JSALTdir=/work/k.church/JSALT-2023/
JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

specter=$JSALTdir/semantic_scholar/embeddings/specter
proposed=$JSALTdir/semantic_scholar/embeddings/proposed
```

We assume that both $specter and $proposed directories contain the following files
<ol>
<li>record_size: 768 for $specter and 280 for $proposed</li>
<li>map.new_to_old.i: map offsets in embedding to corpusIds</li>
<li>map.old_to_new.i: inverse of above</li>
<li>idx.*.i: indexes for approximate nearest neighbors (ANN)</li>
<li>idx.*.i.inv: inverse of above</li>
</ol>

<h2>Installation</h2>

```sh
git clone https://github.com/kwchurch/JSALT_Better_Together
pip install -r requirements.txt
# set environment variable JSALTsrc to the src directory in the repo.
# set environment variable JSALTdir to your local copy of the large data files.
```

<h2>Reading List (and Pre-computed Output)</h2>

See <a href="examples/similar_documents">here</a>, and especially <a href="examples/similar_documents/reading_list">this</a>.
The last example starts with papers we should all be reading, and finds some documents similar to those.


<h2>Examples</h2>

<ol>
<li><a href="doc/semantic_scholar_API.md">Scripts for using Semantic Scholar API</a> (Depends on $JSALTsrc, but not JSALTdir)</li>
<li><a href="doc/find_similar_docs.md">Find similar documents</a> (Depends on both $JSALTsrc and JSALTdir)</li>
</ol>
