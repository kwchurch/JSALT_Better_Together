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

