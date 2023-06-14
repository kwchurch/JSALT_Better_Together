#!/usr/bin/bash

rel=2023-05-09
pushd /work/k.church/semantic_scholar/releases/${rel}/database/citations
zcat ${1} | cut -c1-150 | cut -f4 -d '"' | /work/nlp/j.ortega/paper_recommender/semantic_scholar_specter/time_separations/JSALT_Better_Together/src/fetch_from_semantic_scholar_api.py --fields corpusId,year,publicationDate
popd





