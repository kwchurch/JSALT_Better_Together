# Find Similar Documents

<b>Note</b>, you will need large datasets from
<a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F%7E%2F">Globus</a></li>,
unless you have access to the Discovery Cluster at Northeastern.
<p>
See <a href="../examples/similar_documents/">here</a> for more examples like the following.

```sh
# make sure that $JSALTdir is assigned appropriately

# Here are my enviornment variables:

export JSALTdir=/work/k.church/JSALT-2023/
export JSALTsrc=/work/k.church/githubs/JSALT_Better_Together/src

export specter=$JSALTdir/semantic_scholar/embeddings/specter
export proposed=$JSALTdir/semantic_scholar/embeddings/proposed
export scincl=$JSALTdir/semantic_scholar/embeddings/scincl
```

We assume that $specter, $proposed and $scincl directories contain the following files
<ol>
<li>embedding.f: seqeuence of N*K floats; N is big (10^8)</li>
<li>record_size: K=768 for $specter and K=280 for $proposed</li>
<li>map.new_to_old.i: map offsets in embedding to corpusIds</li>
<li>map.old_to_new.i: inverse of above</li>
<li>idx.*.i: indexes for approximate nearest neighbors (ANN); an index is a permutation on N so papers that are near one another in the index have large cosines</li>
<li>idx.*.i.inv: inverse of above</li>
</ol>

```sh
query=232040593

# Find 3 papers near $query in Specter, and 3 more in Proposed
# This is slow the first time you run it, but it gets faster
# after some warmup

$JSALTsrc/near.sh $query 3

# same as above, but outputs HTML
$JSALTsrc/near.sh $query 3 | $JSALTsrc/tsv_to_html.sh
```

Here is the output from above:

<html><table><tr>
<th>Method</th>
<th>cosS</th>
<th>cosP</th>
<th>paper</th>
</tr>
<tr>
<td>Specter</td>
<td>1.000</td>
<td>1.000</td>
<td><a href="https://www.semanticscholar.org/paper/6d9727f1f058614cada3fe296eeebd8ec4fc512a">522: On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.794</td>
<td>0.957</td>
<td><a href="https://www.semanticscholar.org/paper/bb15f3727f827a3cb88b5d3ca48415c09b40a88f">3: What Language Model to Train if You Have One Million GPU Hours?</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.779</td>
<td>0.976</td>
<td><a href="https://www.semanticscholar.org/paper/8b9d77d5e52a70af37451d3db3d32781b83ea054">117: On the Stability of Fine-tuning BERT: Misconceptions, Explanations, and Strong Baselines</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>1.000</td>
<td>1.000</td>
<td><a href="https://www.semanticscholar.org/paper/6d9727f1f058614cada3fe296eeebd8ec4fc512a">522: On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.615</td>
<td>0.992</td>
<td><a href="https://www.semanticscholar.org/paper/399e7d8129c60818ee208f236c8dda17e876d21f">139: RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.750</td>
<td>0.992</td>
<td><a href="https://www.semanticscholar.org/paper/02fde8bfd9259a4f53316579eb0bf97213559e5c">49: The Radicalization Risks of GPT-3 and Advanced Neural Language Models</a></td>
</tr>
</table></html>

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
<td>1.000</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">5853: DeepWalk: online learning of social representations</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.984</td>
<td>0.827</td>
<td><a href="https://www.semanticscholar.org/paper/93b050f5bf0567a675979cd564cbe66ff9c3a78f">0: Learning of Social Representations</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.809</td>
<td>0.951</td>
<td><a href="https://www.semanticscholar.org/paper/21ee2cc0bf41c1b74efb6104edd4df73416b46c1">2: Topic-aware latent models for representation learning on networks</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.797</td>
<td>0.947</td>
<td><a href="https://www.semanticscholar.org/paper/e294339b402ce055d5a5198becc35b2dbbd20a9a">4: SimWalk: Learning network latent representations with social relation similarity</a></td>
</tr>
<tr>
<td>Specter</td>
<td>0.783</td>
<td>0.033</td>
<td><a href="https://www.semanticscholar.org/paper/bb11bec51c2e069ef0ddba4eb3117c9dbc8a4584">0: Deep Representation Learning on Complex Graphs</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>1.000</td>
<td>1.000</td>
<td><a href="https://www.semanticscholar.org/paper/fff114cbba4f3ba900f33da574283e3de7f26c83">5853: DeepWalk: online learning of social representations</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.771</td>
<td>0.999</td>
https://www.semanticscholar.org/paper/36ee2c8bd605afd48035d15fdc6b8c8842363376<td><a href="https://www.semanticscholar.org/paper/36ee2c8bd605afd48035d15fdc6b8c8842363376">6007: node2vec: Scalable Feature Learning for Networks</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.711</td>
<td>0.998</td>
<td><a href="https://www.semanticscholar.org/paper/0834e74304b547c9354b6d7da6fa78ef47a48fa8">3632: LINE: Large-scale Information Network Embedding</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.664</td>
<td>0.997</td>
<td><a href="https://www.semanticscholar.org/paper/006906b6bbe5c1f378cde9fd86de1ce9e6b131da">1025: A Comprehensive Survey of Graph Embedding: Problems, Techniques, and Applications</a></td>
</tr>
<tr>
<td>Proposed</td>
<td>0.711</td>
<td>0.996</td>
<td><a href="https://www.semanticscholar.org/paper/c0af91371f426ff92117d2ccdadb2032bec23d2c">1157: metapath2vec: Scalable Representation Learning for Heterogeneous Networks</a></td>
</tr>
</table></html>
