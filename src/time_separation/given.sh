rel=2023-05-09
cd /work/k.church/semantic_scholar/releases/$rel/database/citations
mkdir -p graphs
for f in citations.piece.???.gz
do
    b=`basename $f .gz`
    err=graphs/$f.err
    sbatch -p express -t 59 -e $err $JSALTsrc/citations2graph.py $f
done
#/work/k.church/semantic_scholar/releases/2023-05-09/database/citations/graphs
#gft3) [k.church@c0315 graphs]$ cd ..
#(gft3) [k.church@c0315 citations]$ zcat *gz | head | cut -c1-150

#{"citingcorpusid":"17821850","citedcorpusid":"784288","isinfluential":false,"contexts":["Index Terms—Associative memories, bidirectional associative m
#{"citingcorpusid":"221005978","citedcorpusid":"6425905","isinfluential":false,"contexts":null,"intents":null,"updated":"2020-11-01T08:14:11.812Z"}
#{"citingcorpusid":"190533947","citedcorpusid":"26748644","isinfluential":false,"contexts":null,"intents":null,"updated":"2021-10-02T14:07:30.699Z"}

 

#It looks like we will need to join with publication year.  I don’t see a simple relationship between the updated timestamp and the publication year.  The
#year is stored in a different zip file.
#I would like to get publication date with more resolution than year, but that may not be possible.

zcat *gz | head | jq -c '.|{updated,citingcorpusid}'

{"updated":"2020-09-05T19:44:18.575Z","citingcorpusid":"17821850"}

{"updated":"2020-11-01T08:14:11.812Z","citingcorpusid":"221005978"}

{"updated":"2020-05-06T11:36:28.737Z","citingcorpusid":"55922772"}

{"updated":"2020-05-09T14:50:21.354Z","citingcorpusid":"54979738"}

{"updated":"2021-09-23T12:40:31.737Z","citingcorpusid":"219044502"}

{"updated":"2021-10-11T14:55:56.813Z","citingcorpusid":"235417820"}

{"updated":"2020-12-04T21:41:57.113Z","citingcorpusid":"84162210"}

{"updated":"2021-10-02T14:07:30.699Z","citingcorpusid":"190533947"}

{"updated":"2020-12-14T02:48:29.281Z","citingcorpusid":"150486623"}

{"updated":"2020-12-07T00:11:30.313Z","citingcorpusid":"96405497"}

(gft3) [k.church@c0315 citations]$ zcat *gz | head | cut -c1-150 | cut -f4 -d '"' | $JSALTsrc/fetch_from_semantic_scholar_api.py --fields externalIds,year

{'paperId': '0ed78aa20c911709469ac117855b3151b3a4e5e8', 'externalIds': {'MAG': '2184899060', 'DBLP': 'journals/tnn/ChartierB06', 'DOI':
'10.1109/TNN.2005.860855', 'CorpusId': 17821850, 'PubMed': '16526476'}, 'year': 2006}

{'paperId': '477b853362c0eaf51b740a793cb533c067ac9c7b', 'externalIds': {'MAG': '3047033799', 'ArXiv': '2008.02652', 'CorpusId': 221005978}, 'year': 2020}

{'paperId': '1d4849f4b66e1447b3d50f20409ca78210cfadf1', 'externalIds': {'MAG': '2751925012', 'DOI': '10.15226/2471-6529/2/3/00123', 'CorpusId': 55922772},
'year': 2016}

{'paperId': 'ee6d9195bf7c9ec4064841ffc3f9757c022b0fb0', 'externalIds': {'MAG': '2783825974', 'DOI': '10.24247/IJMPERDFEB201867', 'CorpusId': 54979738},
'year': 2018}

{'paperId': '745eeabd9df80a68c6ce60d3234f113b8fa06f65', 'externalIds': {'MAG': '3022957662', 'DOI': '10.1016/j.actamat.2020.04.040', 'CorpusId': 219044502},
'year': 2020}

{'paperId': '0716e006f04a10b930a37a2901da99dbc88acfba', 'externalIds': {'DOI': '10.1002/jcph.1927', 'CorpusId': 235417820, 'PubMed': '34118174'}, 'year':
2021}

{'paperId': 'b8db00a8e62808a170f4ef0ad441e90586ab53d8', 'externalIds': {'MAG': '1996121140', 'DOI': '10.1016/J.FOODCHEM.2009.07.054', 'CorpusId': 84162210},
'year': 2010}

{'paperId': '61be10032113572008575a2ecbe1087a05be845e', 'externalIds': {'MAG': '2951662315', 'DOI': '10.1016/j.theriogenology.2019.06.002', 'CorpusId':
190533947, 'PubMed': '31207473'}, 'year': 2019}

{'paperId': '313ed17912906aad242966fb938b63a3815ee986', 'externalIds': {'MAG': '2914609462', 'DOI': '10.1002/9780470939376.CH6', 'CorpusId': 150486623},
'year': 2015}

{'paperId': '98a43e104587d99a43dccc996a8fabfec8191e49', 'externalIds': {'MAG': '2032637022', 'DOI': '10.1016/J.BEJ.2009.04.007', 'CorpusId': 96405497},
'year': 2009}

 

 

Here is a way to get year for a lot of papers

 

zcat ../papers/*gz | jq -c '{corpusid,year}' | head

{"corpusid":254118849,"year":2019}

{"corpusid":254130601,"year":2018}

{"corpusid":254298902,"year":2022}

{"corpusid":41588354,"year":1987}

{"corpusid":71289147,"year":2002}

{"corpusid":97707419,"year":1962}

{"corpusid":145208848,"year":2010}

{"corpusid":141875306,"year":2015}

{"corpusid":24939538,"year":2009}

{"corpusid":97426290,"year":1995}

 
