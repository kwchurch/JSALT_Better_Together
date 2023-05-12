# Bulk Download from OpenAlex

Documentation for OpenAlex is <a href="https://openalex.org/">here</a>.
<p>
On May 4, 2021, Microsoft announced that <a href="https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/">MAG</a> (Microsoft Academic Graph)
would be retired.  They have subsequently transferred MAG to OpenAlex.
<p>
It is very easy to download data in bulk from OpenAlex.  Here is how I did it.
```sh
cd /work/k.church/openalex
aws s3 sync "s3://openalex" "openalex-snapshot" --no-sign-request
```

The bulk of the data are in works.

```sh
cd /work/k.church/openalex/openalex-snapshot/data; du -h -s *
# 80G	authors
# 84M	concepts
# 55M	institutions
# 19M	merged_ids
# 58M	venues
# 328G	works
```

The lines in these files are also json objects.  Most of the values
are URLs, pointing to openalex.org, with an id that starts with a
capital letter.  A is for authors, C is for concepts, W is for works,
and so on.  One can use this to construct a citation graph.  As for
text, it may be necessary to crawl some of the urls to get abstracts
and full text.

```
zcat /work/k.church/openalex/openalex-snapshot/data/works/*/*gz | sed 1q | jq
# {
#   "id": "https://openalex.org/W2951498914",
#   "doi": "https://doi.org/10.1515/bfp-2019-2055",
#   "ids": {
#     "doi": "https://doi.org/10.1515/bfp-2019-2055",
#     "mag": 2951498914,
#     "openalex": "https://openalex.org/W2951498914"
#   },
#   "mesh": [],
#   "type": "journal-article",
#   "title": "Aspekte digitaler Infrastrukturen : Forschungsdaten im Sonderforschungsbereich 980 „Episteme in Bewegung“: Herausforderungen und Perspektiven",
#   "biblio": {
#     "issue": "2",
#     "volume": "43",
#     "last_page": "331",
#     "first_page": "324"
#   },
#   "concepts": [
#     {
#       "id": "https://openalex.org/C15708023",
#       "level": 1,
#       "score": 0.484445,
#       "wikidata": "https://www.wikidata.org/wiki/Q80083",
#       "display_name": "Humanities"
#     },
#     {
#       "id": "https://openalex.org/C17744445",
#       "level": 0,
#       "score": 0.429106,
#       "wikidata": "https://www.wikidata.org/wiki/Q36442",
#       "display_name": "Political science"
#     },
#     {
#       "id": "https://openalex.org/C144024400",
#       "level": 0,
#       "score": 0.364672,
#       "wikidata": "https://www.wikidata.org/wiki/Q21201",
#       "display_name": "Sociology"
#     },
#     {
#       "id": "https://openalex.org/C2779962280",
#       "level": 3,
#       "score": 0.320098,
#       "wikidata": "https://www.wikidata.org/wiki/Q7433389",
#       "display_name": "SciELO"
#     }
#   ],
#   "host_venue": {
#     "id": "https://openalex.org/V89564548",
#     "url": "https://doi.org/10.1515/bfp-2019-2055",
#     "issn": [
#       "0341-4183",
#       "1865-7648"
#     ],
#     "type": "repository",
#     "is_oa": true,
#     "issn_l": "0341-4183",
#     "license": "cc-by-nc-nd",
#     "version": "submittedVersion",
#     "publisher": "Walter de Gruyter GmbH",
#     "display_name": "Bibliothek Forschung Und Praxis"
#   },
#   "authorships": [
#     {
#       "author": {
#         "id": "https://openalex.org/A2938050355",
#         "orcid": null,
#         "display_name": "Germaine Götzelmann"
#       },
#       "institutions": [
#         {
#           "id": "https://openalex.org/I102335020",
#           "ror": "https://ror.org/04t3en479",
#           "type": "education",
#           "country_code": "DE",
#           "display_name": "Karlsruhe Institute of Technology"
#         }
#       ],
#       "author_position": "first",
#       "raw_affiliation_string": "Karlsruher Institut für Technologie , Steinbuch Centre for Computing , Hermann-von-Helmholtz-Platz 1 , Eggenstein-Leopoldshafen Germany"
#     },
#     {
#       "author": {
#         "id": "https://openalex.org/A2939811429",
#         "orcid": null,
#         "display_name": "Philipp Hegel"
#       },
#       "institutions": [
#         {
#           "id": "https://openalex.org/I75951250",
#           "ror": "https://ror.org/046ak2485",
#           "type": "education",
#           "country_code": "DE",
#           "display_name": "Freie Universität Berlin"
#         }
#       ],
#       "author_position": "middle",
#       "raw_affiliation_string": "Freie Universität Berlin , Sonderforschungsbereich 980 , Schwendenerstraße 8 , Berlin Germany"
#     },
#     {
#       "author": {
#         "id": "https://openalex.org/A705491173",
#         "orcid": null,
#         "display_name": "Michael Krewet"
#       },
#       "institutions": [
#         {
#           "id": "https://openalex.org/I75951250",
#           "ror": "https://ror.org/046ak2485",
#           "type": "education",
#           "country_code": "DE",
#           "display_name": "Freie Universität Berlin"
#         }
#       ],
#       "author_position": "middle",
#       "raw_affiliation_string": "Freie Universität Berlin , Sonderforschungsbereich 980 , Schwendenerstraße 8 , Berlin Germany"
#     },
#     {
#       "author": {
#         "id": "https://openalex.org/A2468068170",
#         "orcid": null,
#         "display_name": "Sibylle Söring"
#       },
#       "institutions": [
#         {
#           "id": "https://openalex.org/I75951250",
#           "ror": "https://ror.org/046ak2485",
#           "type": "education",
#           "country_code": "DE",
#           "display_name": "Freie Universität Berlin"
#         }
#       ],
#       "author_position": "middle",
#       "raw_affiliation_string": "Freie Universität Berlin , Universitätsbibliothek / Center für Digitale Systeme (CeDiS) , Ihnestraße 24 , Berlin Germany"
#     },
#     {
#       "author": {
#         "id": "https://openalex.org/A2124979006",
#         "orcid": null,
#         "display_name": "Danah Tonne"
#       },
#       "institutions": [
#         {
#           "id": "https://openalex.org/I102335020",
#           "ror": "https://ror.org/04t3en479",
#           "type": "education",
#           "country_code": "DE",
#           "display_name": "Karlsruhe Institute of Technology"
#         }
#       ],
#       "author_position": "last",
#       "raw_affiliation_string": "Karlsruher Institut für Technologie , Steinbuch Centre for Computing , Hermann-von-Helmholtz-Platz 1 , Eggenstein-Leopoldshafen Germany"
#     }
#   ],
#   "is_paratext": false,
#   "open_access": {
#     "is_oa": true,
#     "oa_url": "https://www.degruyter.com/downloadpdf/journals/bfup/43/2/article-p324.pdf",
#     "oa_status": "bronze"
#   },
#   "created_date": "2019-06-27",
#   "display_name": "Aspekte digitaler Infrastrukturen : Forschungsdaten im Sonderforschungsbereich 980 „Episteme in Bewegung“: Herausforderungen und Perspektiven",
#   "is_retracted": false,
#   "updated_date": "2022-02-13T20:24:01.189075",
#   "related_works": [],
#   "cited_by_count": 0,
#   "counts_by_year": [],
#   "cited_by_api_url": "https://api.openalex.org/works?filter=cites:W2951498914",
#   "publication_date": "2019-07-01",
#   "publication_year": 2019,
#   "referenced_works": [
#     "https://openalex.org/W2790977509",
#     "https://openalex.org/W2085153875",
#     "https://openalex.org/W2330763494",
#     "https://openalex.org/W2310540074",
#     "https://openalex.org/W2471277952"
#   ],
#   "alternate_host_venues": [
#     {
#       "id": null,
#       "url": "https://edoc.hu-berlin.de/bitstream/18452/20701/1/AR_3284_Goetzelmann_Preprints_BFP_2019.pdf",
#       "type": "repository",
#       "is_oa": true,
#       "license": "cc-by-nc-nd",
#       "version": "submittedVersion",
#       "display_name": "Humboldt University of Berlin - edoc Publication server"
#     }
#   ],
#   "abstract_inverted_index": {}
# }
```