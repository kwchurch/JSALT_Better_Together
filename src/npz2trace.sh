#!/bin/sh

infile=$1
tmpdir=$2.$$.`hostname`
topN=$3
K=$4
outdir=$5

mkdir -p $outdir

mkdir -p $tmpdir

$JSALTsrc/npz2npy.py $infile $tmpdir/emb.npy

G=$tmpdir/G
$JSALTsrc/brute_force_lookup.py --topN $topN --embedding $tmpdir/emb.npy > $G

$JSALTsrc/txt2npz.py -o $G.npz --make_symmetric < $G

$JSALTsrc/new_shrink_matrix.py --graph $G.npz -o $G.shrunk

out=$G.shrunk.G2.U.V2.K$K
tmp=$G.tmp
$JSALTsrc/prefactor_graph.py -G $G.shrunk.G2.npz -O $out -K $K
$JSALTsrc/ProNE_chebyshev.py -G $G.shrunk.G2.npz -U $out.npy --temp_file_prefix $tmp --iteration 0
$JSALTsrc/ProNE_chebyshev.py -G $G.shrunk.G2.npz -U $out.npy --temp_file_prefix $tmp --iteration 1

U=$out.npy
for i in 1
do
$JSALTsrc/ProNE_finish.py -G $G.npz -U $U --temp_file_prefix $tmp -O $U.finished.i$i --iteration $i
$JSALTsrc/trace_and_quantiles.py "$U.finished.i$i"*
done

mv "$U.finished.i$i"* $outdir
mv $G.npz $G.shrunk.npz $outdir
rm -rf $tmpdir
