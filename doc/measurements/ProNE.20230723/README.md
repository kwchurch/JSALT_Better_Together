# Measurements of ProNE by bin

<ol>
<li><b>f</b>: use ProNE vectors for the two input corpus ids</li>
<li><b>fhat</b>: use the centroid approximation to estiamte vectors for the two input corpus ids</li>
<li><b>ensemble</b>: use f when it is available, and otherwise use fhat</li>
</ol>

<h2>Materials</h2>

See walk_with_bins on <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Feval%2F">Globus</a>.  If you have access to the Northeastern cluster, see $JSALTdir/semantic_scholar/eval/walk_with_bins.
There are splits of this data: walk.??.  Each of these splits is about 50k lines.  The first column is a distance
on the graph followed by two corpus ids (and their bins).
<p>
Task: input a pair of corpus ids and output 0 or 1 (either the first paper references the second, or not).  That is, the distance
is either 1 or more than 1.  The negatives are harder than random since all of these pairs are near one another in the graph.
<p>
Train on some bins,
and test on others.  We hope to show that short-term forecasting is easier than long-term forecasting.

<h2>Results</h2>

There are files like this many values of $bin:

<ol>
<li>f: $JSALTdir/semantic_scholar/embeddings/proposed/bins/$bin/walk_pieces/never/walk12.??<li>
<li>fhat: $JSALTdir/semantic_scholar/embeddings/proposed/bins/$bin/walk_pieces/always/walk12.??<li>
<li>ensemble: $JSALTdir/semantic_scholar/embeddings/proposed/bins/$bin/walk_pieces/when_necessary/walk12.??<li>
</ol>

The difference between f, fhat and ensemble involves the centroid approximation: fhat(d) = sum f(r), where r is a reference of d.
<p>
We either use this approximation: never (for f), always (for fhat), or when_necessary (for ensemble).
<p>
These files were computed with <a href="https://github.com/kwchurch/JSALT_Better_Together/blob/main/src/pairs_to_cos.py">pairs_to_cos</a>.
That program has an argument, use_references, which should be set to never, always or when_neceessary.
<p>
pairs_to_cosine inputs two corpus ids and outputs their cosine (or -1 if NA).

<p>

<h2>Observations</h2>
<ol>
<li><b>Better Together</b>: The ensemble method has better coverage than both f and fhat.</li>
<li>Coverage increases with bin number</li>
<li>Coverage of fhat assymptotes around 75%, because we have references for aobut 75% of the pairs in the sample</li>
</ol>


<img src="coverage3.jpg" alt="Coverage for f, fhat and ensemble methods" width="600" />
<p>
The following two plots are a deep dive into bin 036.
<p>
<img src="walk.ab.036.boxplots.jpg" alt="Output ProNE Embeddings are 200x larger than the input citation graphs" width="600" />
<p>
<img src="walk.ab.036.pairs.jpg" alt="Output ProNE Embeddings are 200x larger than the input citation graphs" width="600" />
<p>

