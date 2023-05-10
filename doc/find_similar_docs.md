# Find Similar Documents

```sh
# make sure that $JSALTdir is assigned appropriately

query=232040593

# Find 3 papers near $query in Specter, and 3 more in Proposed
# This is slow the first time you run it, but it gets faster
# after some warmup

$JSALTsrc/near.sh $query 5

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
