# Bulk Download from Semantic Scholar API

Semantic Scholar's documentation is <a href="semantic_scholar/releases/2022-12-02/database/">here</a>.
There is a link there for the latest release. 

On the Northeastern Discovery Cluster, there are directories here:

```sh
ls -d /work/k.church/semantic_scholar/releases/*/database $JSALTdir/semantic_scholar/releases/*/database 
# /work/k.church/semantic_scholar/releases/2022-05-31/database
# /work/k.church/semantic_scholar/releases/2022-08-23/database
# /work/k.church/semantic_scholar/releases/2022-11-22/database
# /work/k.church/semantic_scholar/releases/2022-12-02/database
# /work/k.church/semantic_scholar/releases/2023-05-09/database
# /work/k.church/JSALT-2023/semantic_scholar/releases/2022-12-02/database
# /work/k.church/JSALT-2023/semantic_scholar/releases/2023-05-09/database
# /work/k.church/JSALT-2023/semantic_scholar/releases/2023-06-20/database
```

/work/k.church/JSALT-2023 is available via <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2F">Globus</a>, so you can find some of the files above
on <a href="https://app.globus.org/file-manager?origin_id=1ef9019c-eac0-11ed-9ba9-c9bb788c490e&origin_path=%2F~%2Fsemantic_scholar%2Freleases%2F2023-06-20%2Fdatabase%2F">here</a>.

<ol>
<li>authors: a json object for each author with authorid, name, papercount, citationcount, hindex (and more)</li>
<li>papers: a json object for each paper, with: externalIds, title, authors, fields of study, venues (and more)</li>
<li>abstracts: a json object for each paper with an abstract (and more)</li>
<li>tldrs (too long; didn't read): a json object for each paper with a summary (typically a substring from the abstract)</li>
<li>citations: a json object for each paper with two ids (citingcorpusid and citedcorpusid), contexts (citing sentences), isinfluential (and more)</li>
<li>embeddings: a json object for each paper with a specter@v0.1.1 vector of 768 floats</li>
<li>s2orc: a json object for each paper with annotations from s2 (semantic scholar)</li>
</ol>

jq is a useful program for looking at these objects
<p>
-c arg (compact) prints one line for each json object
<p>
This pulls the two fields, corpusid and title:

```sh
zcat papers/*gz | jq -c '. | {corpusid,title}' | head | cut -c1-100
{"corpusid":254118849,"title":"A genetic-phenotypic classification for syndromic micrognathia"}
{"corpusid":254130601,"title":"Invasion and translocation of uropathogenic Escherichia coli isolated
{"corpusid":254298902,"title":"Hydrothermal aging mechanism of K/CeO2 catalyst in soot catalytic com
{"corpusid":41588354,"title":"Antihypertensive effect of a renin inhibitor in marmosets with a segme
{"corpusid":71289147,"title":"Hirschsprung disease: A component of the familial cancer syndrome mult
{"corpusid":97707419,"title":"An apparatus for aeration of tissue cells in suspended culture with co
{"corpusid":145208848,"title":"Review: Swing from a Small Island: the story of Leslie Thompson"}
{"corpusid":141875306,"title":"Observations on the development of ethical culture"}
{"corpusid":24939538,"title":"Enzymatic re-esterification of lower glycerides from soybean oil with
{"corpusid":97426290,"title":"A Model for Interdiffusion at Interfaces of Polymers with Dissimilar P
```

Under each of these directories, there are 30 gzip files.  Each of these gzip
files contains a json line for each corpusid.  Here is an example of
the line for corpusid 148308872:

```sh
zcat abstracts/*gz | sed 1q | jq 
# {
#   "corpusid": 148308872,
#   "openaccessinfo": {
#     "externalids": {
#       "MAG": "2370633486",
#       "ACL": null,
#       "DOI": null,
#       "PubMedCentral": null,
#       "ArXiv": null
#     },
#     "license": null,
#     "url": null,
#     "status": null
#   },
#   "abstract": "Ideological and political work is very important in economical work and any other work.The direction of ideological and political w ork is a presupposition of its effect and initiative.So,we should analyze and st u dy the ideological and political work seriously.To study the direction,we must m ake the system of the direction clear first.According to ideological and politic al education process,the direction system is constituted of the ideological and political education aim and the direction of work,object,time,spac e,method,way and content.",
#   "updated": "2022-02-09T04:57:41.407Z"
# }
```

Note: <a href="https://stedolan.github.io/jq/">jq</a> is a really useful function for manipulating json objects on the command line.


Here is a summary of databases (excluding the abstract database shown above).  Most of these fields
can also be requested via ad hoc queries, as discussed <a href="semantic_scholar_API.md">here</a>.

```sh
cd /work/k.church/semantic_scholar/releases/2022-12-02/database
for f in */*.001.gz 
do
echo $f
zcat $f | sed 1q | jq  | cut -c1-200
done

# authors/authors.piece.001.gz
# {
#   "authorid": "2064159550",
#   "externalids": null,
#   "url": "https://www.semanticscholar.org/author/2064159550",
#   "name": "Andrea Karla Ferreira Nunes",
#   "aliases": null,
#   "affiliations": null,
#   "homepage": null,
#   "papercount": 5,
#   "citationcount": 1,
#   "hindex": 1,
#   "updated": "2021-11-28T09:26:51.282Z"
# }
# embeddings/embeddings.piece.001.gz
# {
#   "corpusid": 188918598,
#   "model": "specter@v0.1.1",
#   "vector": "[1.264845848083496, -0.6985993981361389, 0.2853028178215027, 2.4109959602355957, -0.8213783502578735, -2.2281577587127686, 1.6246418952941895, -3.864623546600342, 1.7828009128570557, 0.77
#   "updated": "2021-10-23T03:32:37Z"
# }
# papers/papers.piece.001.gz
# {
#   "corpusid": 210683441,
#   "externalids": {
#     "ACL": null,
#     "DBLP": null,
#     "ArXiv": null,
#     "MAG": "577300514",
#     "CorpusId": "210683441",
#     "PubMed": null,
#     "DOI": null,
#     "PubMedCentral": null
#   },
#   "url": "https://www.semanticscholar.org/paper/69552edc28c55ba3cacf1a21388971886bd7c802",
#   "title": "Constitution and rights in the early American republic",
#   "authors": [
#     {
#       "authorId": "47473355",
#       "name": "W. E. Nelson"
#     },
#     {
#       "authorId": "49249891",
#       "name": "R. Palmer"
#     }
#   ],
#   "venue": "",
#   "year": 1987,
#   "referencecount": 0,
#   "citationcount": 0,
#   "influentialcitationcount": 0,
#   "isopenaccess": false,
#   "s2fieldsofstudy": [
#     {
#       "category": "History",
#       "source": "s2-fos-model"
#     },
#     {
#       "category": "Political Science",
#       "source": "external"
#     }
#   ],
#   "publicationtypes": null,
#   "publicationdate": null,
#   "journal": {
#     "name": "",
#     "volume": "",
#     "pages": null
#   },
#   "updated": "2022-03-09T21:12:48.895Z"
# }
# s2orc/s2orc.piece.001.gz
# {
#   "corpusid": 253878775,
#   "externalids": {
#     "arxiv": null,
#     "mag": null,
#     "acl": null,
#     "pubmed": "36429152",
#     "pubmedcentral": "9689397",
#     "dblp": null,
#     "doi": "10.3390/foods11223559"
#   },
#   "content": {
#     "source": {
#       "pdfurls": null,
#       "pdfsha": "480ff89592fb2fef480e87dbcf8a082cc06df5d4",
#       "oainfo": {
#         "license": "CCBY",
#         "openaccessurl": "https://www.mdpi.com/2304-8158/11/22/3559/pdf?version=1667983056",
#         "status": "GOLD"
#       }
#     },
#     "text": "\n\nPublished: 9 November 2022\n\n\nDepartment of Pharmacy\nG. d'Annunzio University of Chieti-Pescara\n66013ChietiItaly\n\n\nDepartment of Pharmacy\nUniversity of Pisa\n56126PisaItaly\n\
#     "annotations": {
#       "abstract": "[{\"end\":1171,\"start\":848}]",
#       "author": "[{\"end\":114,\"start\":30},{\"end\":173,\"start\":115},{\"end\":262,\"start\":174},{\"end\":388,\"start\":263},{\"end\":492,\"start\":389},{\"end\":662,\"start\":493},{\"end\":715,\"
#       "authoraffiliation": "[{\"end\":113,\"start\":31},{\"end\":172,\"start\":116},{\"end\":261,\"start\":175},{\"end\":387,\"start\":264},{\"end\":491,\"start\":390},{\"end\":661,\"start\":494},{\"e
#       "authorfirstname": null,
#       "authorlastname": null,
#       "bibauthor": "[{\"end\":45797,\"start\":45788},{\"end\":45806,\"start\":45797},{\"end\":45814,\"start\":45806},{\"end\":45823,\"start\":45814},{\"end\":45833,\"start\":45823},{\"end\":45842,\"st
#       "bibauthorfirstname": "[{\"end\":45789,\"start\":45788},{\"end\":45798,\"start\":45797},{\"end\":45800,\"start\":45799},{\"end\":45807,\"start\":45806},{\"end\":45809,\"start\":45808},{\"end\":4
#       "bibauthorlastname": "[{\"end\":45795,\"start\":45790},{\"end\":45804,\"start\":45801},{\"end\":45812,\"start\":45810},{\"end\":45821,\"start\":45818},{\"end\":45831,\"start\":45827},{\"end\":45
#       "bibentry": "[{\"attributes\":{\"doi\":\"10.3390/foods8070246\",\"id\":\"b0\"},\"end\":46104,\"start\":45714},{\"attributes\":{\"doi\":\"10.3390/antiox8090405\",\"id\":\"b1\",\"matched_paper_id\
#       "bibref": "[{\"attributes\":{\"ref_id\":\"b0\"},\"end\":1347,\"start\":1344},{\"attributes\":{\"ref_id\":\"b1\"},\"end\":1440,\"start\":1437},{\"attributes\":{\"ref_id\":\"b2\"},\"end\":1454,\"s
#       "bibtitle": "[{\"end\":46253,\"start\":46106},{\"end\":46718,\"start\":46590},{\"end\":47206,\"start\":47112},{\"end\":47578,\"start\":47474},{\"end\":47974,\"start\":47898},{\"end\":48668,\"sta
#       "bibvenue": "[{\"end\":45786,\"start\":45714},{\"end\":46330,\"start\":46318},{\"end\":46832,\"start\":46823},{\"end\":47278,\"start\":47267},{\"end\":47669,\"start\":47648},{\"end\":48033,\"sta
#       "figure": "[{\"attributes\":{\"id\":\"fig_2\"},\"end\":37565,\"start\":37083},{\"attributes\":{\"id\":\"fig_4\"},\"end\":37851,\"start\":37566},{\"attributes\":{\"id\":\"fig_5\"},\"end\":38026,\
#       "figurecaption": "[{\"end\":37565,\"start\":37085},{\"end\":37851,\"start\":37579},{\"end\":38026,\"start\":37865},{\"end\":38110,\"start\":38040},{\"end\":38194,\"start\":38124},{\"end\":38278,
#       "figureref": "[{\"attributes\":{\"ref_id\":\"fig_4\"},\"end\":12710,\"start\":12702},{\"attributes\":{\"ref_id\":\"fig_7\"},\"end\":16009,\"start\":15999},{\"attributes\":{\"ref_id\":\"fig_10\"}
#       "formula": "[{\"attributes\":{\"id\":\"formula_0\"},\"end\":15375,\"start\":15364}]",
#       "paragraph": "[{\"end\":1727,\"start\":1187},{\"end\":2199,\"start\":1786},{\"end\":3833,\"start\":2299},{\"end\":4331,\"start\":3937},{\"end\":5347,\"start\":4333},{\"end\":5897,\"start\":5349}
#       "publisher": null,
#       "sectionheader": "[{\"attributes\":{\"n\":\"1.\"},\"end\":1185,\"start\":1173},{\"attributes\":{\"n\":\"2.\"},\"end\":1751,\"start\":1730},{\"attributes\":{\"n\":\"2.1.\"},\"end\":1784,\"start\"
#       "table": "[{\"end\":42139,\"start\":41132},{\"end\":43293,\"start\":42220},{\"end\":43596,\"start\":43370},{\"end\":44508,\"start\":43673},{\"end\":45301,\"start\":44608},{\"end\":45712,\"start\
#       "tableref": "[{\"attributes\":{\"ref_id\":\"tab_1\"},\"end\":11980,\"start\":11972},{\"attributes\":{\"ref_id\":\"tab_0\"},\"end\":12122,\"start\":12115},{\"attributes\":{\"ref_id\":\"tab_0\"},\
#       "title": null,
#       "venue": null
#     }
#   },
#   "updated": "2022-11-27T07:42:50Z"
# }
# tldrs/tldrs.piece.001.gz
# {
#   "corpusid": 2892064,
#   "model": "tldr@v2.0.0",
#   "text": "Het is allerminst mijn bedoeling de invoering van \"de combines in ons land op grond van het bovenstaande overal en onder alle omstandigheden af te raden\", wel eenigszins anders zijn dan i
# }
```