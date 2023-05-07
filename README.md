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

The folowing will output the table below:

```sh
$JSALTsrc/near.sh 3051291 | $JSALTsrc/tsv_to_html.sh
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
<td>0.999257</td>
<td><a href="https://www.semanticscholar.org/paper/36ee2c8bd605afd48035d15fdc6b8c8842363376">6007: node2vec: Scalable Feature Learning for Networks</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.809</td>
<td>0.998433</td>
<td><a href="https://www.semanticscholar.org/paper/0834e74304b547c9354b6d7da6fa78ef47a48fa8">3632: LINE: Large-scale Information Network Embedding</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.797</td>
<td>0.996686</td>
<td><a href="https://www.semanticscholar.org/paper/006906b6bbe5c1f378cde9fd86de1ce9e6b131da">1025: A Comprehensive Survey of Graph Embedding: Problems, Techniques, and Applications</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.783</td>
<td>0.996354</td>
<td><a href="https://www.semanticscholar.org/paper/c0af91371f426ff92117d2ccdadb2032bec23d2c">1157: metapath2vec: Scalable Representation Learning for Heterogeneous Networks</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.775</td>
<td>0.996268</td>
<td><a href="https://www.semanticscholar.org/paper/908272f8e6340971600148d4e73f50e1e8843aaf">570: Network Embedding as Matrix Factorization: Unifying DeepWalk, LINE, PTE, and node2vec</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.773</td>
<td>0.996181</td>
<td><a href="https://www.semanticscholar.org/paper/9d9d33843d018a77bad7f40da8f27671d29cd776">348: HIN2Vec: Explore Meta-paths in Heterogeneous Information Networks for Representation Learning</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.770</td>
<td>0.995577</td>
<td><a href="https://www.semanticscholar.org/paper/fce14c6aa64e888456256ac6796744683165a0ff">748: Network Representation Learning with Rich Text Information</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.769</td>
<td>0.995186</td>
<td><a href="https://www.semanticscholar.org/paper/454a69d2b93049c794247e1e4dc2e4b590172dae">48: dynnode2vec: Scalable Dynamic Network Embedding</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.769</td>
<td>0.995123</td>
<td><a href="https://www.semanticscholar.org/paper/ce840188f3395815201b7da49f9bb40d24fc046a">668: A Survey on Network Embedding</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.769</td>
<td>0.994736</td>
<td><a href="https://www.semanticscholar.org/paper/1a37f07606d60df365d74752857e8ce909f700b3">632: Deep Neural Networks for Learning Graph Representations</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.764</td>
<td>0.994723</td>
<td><a href="https://www.semanticscholar.org/paper/e75491aba169909922c6e836a39037a5e6be426e">111: Don't Walk, Skip!: Online Learning of Multi-scale Network Embeddings</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.761</td>
<td>0.994583</td>
<td><a href="https://www.semanticscholar.org/paper/0f7f5679615effcc4c9b98cf2deb17c30744a6d7">743: struc2vec: Learning Node Representations from Structural Identity</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.760</td>
<td>0.994573</td>
<td><a href="https://www.semanticscholar.org/paper/707defa78c0e5529c17fda92ce7b33f0b6674612">126: Dynamic Network Embedding : An Extended Approach for Skip-gram based Network Embedding</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.754</td>
<td>0.994227</td>
<td><a href="https://www.semanticscholar.org/paper/6b183d2297cb493a57dbc875689ab2430d870043">193: Task-Guided and Path-Augmented Heterogeneous Network Embedding for Author Identification</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.754</td>
<td>0.994024</td>
<td><a href="https://www.semanticscholar.org/paper/c2fd72cb2a77941e655b5d949d0d59b01e173c3b">1118: GraRep: Learning Graph Representations with Global Structural Information</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.753</td>
<td>0.993894</td>
<td><a href="https://www.semanticscholar.org/paper/390bc9d41c1169d316accd993fc715b8ed17f269">117: Scalable Graph Embedding for Asymmetric Proximity</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.751</td>
<td>0.993690</td>
<td><a href="https://www.semanticscholar.org/paper/98b8c1fa10292c46801eec609e8f9da83f18e228">69: MetaGraph2Vec: Complex Semantic Path Augmented Heterogeneous Network Embedding</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.747</td>
<td>0.993436</td>
<td><a href="https://www.semanticscholar.org/paper/73d9ee3238a872af94d5a03f4d951234c90037ac">108: An Attention-based Collaboration Framework for Multi-View Network Representation Learning</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.745</td>
<td>0.993429</td>
<td><a href="https://www.semanticscholar.org/paper/71bab0bb655a9bf7a7ef8a2308db1097111fd7d1">81: Easing Embedding Learning by Comprehensive Transcription of Heterogeneous Information Networks</a></td>
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
<tr>
<td>Proposed</td>
<td>0.749</td>
<td>0.996268</td>
<td><a href="https://www.semanticscholar.org/paper/908272f8e6340971600148d4e73f50e1e8843aaf">570: Network Embedding as Matrix Factorization: Unifying DeepWalk, LINE, PTE, and node2vec</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.768</td>
<td>0.996181</td>
<td><a href="https://www.semanticscholar.org/paper/9d9d33843d018a77bad7f40da8f27671d29cd776">348: HIN2Vec: Explore Meta-paths in Heterogeneous Information Networks for Representation Learning</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.792</td>
<td>0.995577</td>
<td><a href="https://www.semanticscholar.org/paper/fce14c6aa64e888456256ac6796744683165a0ff">748: Network Representation Learning with Rich Text Information</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.693</td>
<td>0.995186</td>
<td><a href="https://www.semanticscholar.org/paper/454a69d2b93049c794247e1e4dc2e4b590172dae">48: dynnode2vec: Scalable Dynamic Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.655</td>
<td>0.995123</td>
<td><a href="https://www.semanticscholar.org/paper/ce840188f3395815201b7da49f9bb40d24fc046a">668: A Survey on Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.777</td>
<td>0.994736</td>
<td><a href="https://www.semanticscholar.org/paper/1a37f07606d60df365d74752857e8ce909f700b3">632: Deep Neural Networks for Learning Graph Representations</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.840</td>
<td>0.994723</td>
<td><a href="https://www.semanticscholar.org/paper/e75491aba169909922c6e836a39037a5e6be426e">111: Don't Walk, Skip!: Online Learning of Multi-scale Network Embeddings</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.678</td>
<td>0.994583</td>
<td><a href="https://www.semanticscholar.org/paper/0f7f5679615effcc4c9b98cf2deb17c30744a6d7">743: struc2vec: Learning Node Representations from Structural Identity</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.734</td>
<td>0.994573</td>
<td><a href="https://www.semanticscholar.org/paper/707defa78c0e5529c17fda92ce7b33f0b6674612">126: Dynamic Network Embedding : An Extended Approach for Skip-gram based Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.627</td>
<td>0.994227</td>
<td><a href="https://www.semanticscholar.org/paper/6b183d2297cb493a57dbc875689ab2430d870043">193: Task-Guided and Path-Augmented Heterogeneous Network Embedding for Author Identification</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.765</td>
<td>0.994024</td>
<td><a href="https://www.semanticscholar.org/paper/c2fd72cb2a77941e655b5d949d0d59b01e173c3b">1118: GraRep: Learning Graph Representations with Global Structural Information</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.724</td>
<td>0.993894</td>
<td><a href="https://www.semanticscholar.org/paper/390bc9d41c1169d316accd993fc715b8ed17f269">117: Scalable Graph Embedding for Asymmetric Proximity</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.674</td>
<td>0.993690</td>
<td><a href="https://www.semanticscholar.org/paper/98b8c1fa10292c46801eec609e8f9da83f18e228">69: MetaGraph2Vec: Complex Semantic Path Augmented Heterogeneous Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.704</td>
<td>0.993436</td>
<td><a href="https://www.semanticscholar.org/paper/73d9ee3238a872af94d5a03f4d951234c90037ac">108: An Attention-based Collaboration Framework for Multi-View Network Representation Learning</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.682</td>
<td>0.993429</td>
<td><a href="https://www.semanticscholar.org/paper/71bab0bb655a9bf7a7ef8a2308db1097111fd7d1">81: Easing Embedding Learning by Comprehensive Transcription of Heterogeneous Information Networks</a></td>
</tr>
</table></html>
