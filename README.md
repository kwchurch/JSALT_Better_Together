# JSALT_Better_Together

<a href="https://jsalt2023.univ-lemans.fr/en/better-together-text-context.html">Better Together: Text + Context</a>

To install
```sh
git clone https://github.com/kwchurch/JSALT_Better_Together
pip install -r requirements.txt
```

Some examples of usage

```sh
echo 232040593 | src/fetch_from_semantic_scholar_api.py --fields title,externalIds
# {'paperId': '6d9727f1f058614cada3fe296eeebd8ec4fc512a', '
#              externalIds': {'DBLP': 'conf/fat/BenderGMS21', 'DOI': '10.1145/3442188.3445922', 'CorpusId': 232040593},
#              'title': 'On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜'}}`
```

Some useful fields:
<ol>
<li>title</li>
<li>abstract</li>
<li>authors</li>
<li>externalIds</li>
<li>citationCount</li>
<li>referenceCount</li>
<li>citations</li>
<li>references</li>
<li>embedding</li>
<li>venue</li>
<li>fieldsOfStudy</li>
<li>s2fieldsOfStudy</li>
<li>openAccessPdf</li>
<li>tldr</li>
</ol>


```sh
echo '232040593	On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?' | 
src/text_to_embedding.py -o /tmp/foobar
```

This will read lines (tab delimited) with a corpusId in column 1 and text in column 2;
output goes to /tmp/foobar.kwc.i and /tmp/foobar.kwc.f.
The first file is a sequence of int32 (one for each input line);
The second file is a sequence float32 (one record of K=768 for each input line).
You can process these binary files in C or with numpy.fromfile.
There is an optional --model argument which allows you to specify models from HuggingFace.

<p>

The following will output up to 1000 lines, one for each reference.
It will also output up to 1000 lines, one for each citation.  The
first line is a summary with the count of references and citations
(which may exceed 1000).  Subsequent lines start with either
"reference" or "citation".  The next two ids are the corpusId for the
query and the reference/citation.  The last two columns are the number
of citations and the title of the paper.

```sh
echo 232040593 | src/fetch_references_and_citations.py | head
query	156 references	1113 citations	On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜
reference	232040593	243950006	2	The Five Hundred Year Rebellion: Indigenous Movements and the Decolonization of History in Bolivia
reference	232040593	243615599	57	The Argonauts
reference	232040593	231573431	674	Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity
reference	232040593	230435736	400	The Pile: An 800GB Dataset of Diverse Text for Language Modeling
reference	232040593	229156229	515	Extracting Training Data from Large Language Models
reference	232040593	225040574	843	mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer
reference	232040593	220265858	392	GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
reference	232040593	220265500	193	Large image datasets: A pyrrhic win for computer vision?
reference	232040593	219530686	90	Detecting Emergent Intersectional Biases: Contextualized Word Embeddings Contain a Distribution of Human-like Biases
```

The folowing will output the table below.  The first argument is a
corpusId and the second argument is the number of candidates to
output.

```sh
$JSALTsrc/near.sh 3051291 5 | $JSALTsrc/tsv_to_html.sh
```

<html><table><tr>
<th>Method</th>
<th>cosS</th>
<th>cosP</th>
<th>paper</th>
</tr>
<tr>
<td>Specter</td>
<td>1.000</td>
<td>1.000000</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">5853: DeepWalk: online learning of social representations</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.984</td>
<td>0.826657</td>
<td><a href="https://www.semanticscholar.org/paper/93b050f5bf0567a675979cd564cbe66ff9c3a78f">0: Learning of Social Representations</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.809</td>
<td>0.951167</td>
<td><a href="https://www.semanticscholar.org/paper/21ee2cc0bf41c1b74efb6104edd4df73416b46c1">2: Topic-aware latent models for representation learning on networks</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.797</td>
<td>0.946531</td>
<td><a href="https://www.semanticscholar.org/paper/e294339b402ce055d5a5198becc35b2dbbd20a9a">4: SimWalk: Learning network latent representations with social relation similarity</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.783</td>
<td>0.033244</td>
<td><a href="https://www.semanticscholar.org/paper/bb11bec51c2e069ef0ddba4eb3117c9dbc8a4584">0: Deep Representation Learning on Complex Graphs</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>1.000</td>
<td>1.000000</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">5853: DeepWalk: online learning of social representations</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.771</td>
<td>0.999257</td>
<td><a href="https://www.semanticscholar.org/paper/36ee2c8bd605afd48035d15fdc6b8c8842363376">6007: node2vec: Scalable Feature Learning for Networks</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.711</td>
<td>0.998433</td>
<td><a href="https://www.semanticscholar.org/paper/0834e74304b547c9354b6d7da6fa78ef47a48fa8">3632: LINE: Large-scale Information Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.664</td>
<td>0.996686</td>
<td><a href="https://www.semanticscholar.org/paper/006906b6bbe5c1f378cde9fd86de1ce9e6b131da">1025: A Comprehensive Survey of Graph Embedding: Problems, Techniques, and Applications</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.711</td>
<td>0.996354</td>
<td><a href="https://www.semanticscholar.org/paper/c0af91371f426ff92117d2ccdadb2032bec23d2c">1157: metapath2vec: Scalable Representation Learning for Heterogeneous Networks</a></td>
</tr>
</table></html>
