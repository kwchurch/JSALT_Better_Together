#!/usr/bin/bash

mydir=`pwd`
rel=2023-05-09
outd=/work/nlp/j.ortega/paper_recommender/semantic_scholar_specter/time_separations/citations_by_year/$rel/
mkdir -p $outd
pushd /work/k.church/semantic_scholar/releases/${rel}/database/citations
for f in citations.piece.???.gz
    do
        serr=$outd/$f.err
        sout=$outd/$f.out
        sbatch -p express -t 59 -e $serr -o $sout $mydir/process_citations.sh $f
    done
popd



