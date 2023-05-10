# Notation

<ol>
<li>Let <i>N</i> = 200M be the number of nodes (documents) in the collection</li>
<li>Let <i>E</i> = 2B be the number of edges (citations) </li>
<li>Let <i>G=(N,E)</i> be a graph with <i>N</i> nodes and <i>E</i> edges.  An example of a graph is $JSALTdir/citations.G.npz; see <a href="graph.md">graph documentation</a> for an exmaple.</li>
<li>Let <i>K</i> be the number of hidden dimensions</li>
<li>Let <i>d</i> be a document (not hidden dimensions)</li>
<li>Let <i>s</i> be a string</li>
<li>Let <i>v</i> be a vector of length <i>K</i></li>
<li>Let <i>f</i> be a model.  BERT-like models take strings as args,
<i>f(s)=v</i>.  We will also consider models that take documents as
arguments, <i>f(d)=v</i>.  In both cases, the output is a vector, <i>v</i>.</li>
<i>Let <i>f^{-1}(v) = d</i> be the inverse of <i>f(d)=v</i>.  
<li>Let <i>M</i> be an embedding, a matrix of N by K.  The i-th row of <i>M</i> is <i>f(d[i])</i>.  Examples of embeddings:
$proposed/embedding.f and $specter/embedding.f.
 </li>
</ol>