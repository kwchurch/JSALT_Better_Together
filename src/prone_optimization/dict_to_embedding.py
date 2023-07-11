#!/usr/bin/env python

import numpy as np
import csrgraph as cg
import sys,os,socket,argparse,time
import nodevectors

#from memory_profiler import profile

#print('dict_to_embedding.py: ' + str(sys.argv), file=sys.stderr)

t0 = time.time()

# echo hostname = `hostname` 1>&2
# echo SLURM_JOB_ID = $SLURM_JOB_ID 1>&2
# echo SLURM_ARRAY_TASK_ID = $SLURM_ARRAY_TASK_ID 1>&2

#print('dict_to_embedding: hostname = ' + str(socket.gethostname()), file=sys.stderr)
#print('dict_to_embedding: SLURM_JOB_ID = ' + str(os.getenv('SLURM_JOB_ID')), file=sys.stderr)
#print('dict_to_embedding: SLURM_ARRAY_TASK_ID = ' + str(os.getenv('SLURM_ARRAY_TASK_ID')), file=sys.stderr)

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="output file", required=True)
parser.add_argument("-i", "--input_edge_list", help="input text file (one line for each edge)", default=None)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
parser.add_argument("-K", "--components", type=int, help="hidden dimensions [defaults = 32]", default=32)
parser.add_argument("-T", "--threads", type=int, help="number of threads [defaults = 20] (applies to methods: GGVec and Glove", default=20)
parser.add_argument("-O", "--order", type=int, help="order [defaults = 5] (applies to methods: GGVec and GraRep", default=5)
parser.add_argument("-d", "--delimiter", help="defaults to tab", default='\t')
parser.add_argument("-m", "--method", help="one of GGVec|GraRep|Glove|ProNE|ProNE_prefactorization", default='ProNE')
parser.add_argument("-t", '--transpose', action='store_true')
parser.add_argument("-F", '--features_matrix', help='for ProNE, result of pre_factorization', default=None)
# parser.add_argument("-s", "--save_svd", help="save a svd model", action='store_true')
# parser.add_argument("-l", "--load_svd", help="load an svd model", action='store_true')
# parser.add_argument("-f", "--svd_file", help="filename/dirname to load or save", default=".")
args = parser.parse_args()

assert (args.input_graph is None) != (args.input_edge_list is None), 'please specify either --input_edge_list or --input_graph (but not both)'

def strip_suffix(s, suffixes):
    for suf in suffixes:
        if s.endswith(suf):
            return s[0:-len(suf)]
    return s

def method2model():
    m = args.method
    K = args.components
    #print('# K = %d, time: %0.2f' % (K, (time.time() - t0)), file=sys.stderr)
    T = args.threads
    O = args.order
    # s = args.save_svd
    # l = args.load_svd
    # f = args.svd_file
    if m == 'GGVec':
        return nodevectors.GGVec(n_components=K, threads=T, order=O)
    elif m == 'GraRep':
        return nodevectors.GraRep(n_components=K, order=O)
    elif m ==  'Glove':
        return nodevectors.Glove(n_components=K, threads=T)
    elif m == 'ProNE':
        return nodevectors.ProNE(n_components=K)
    # elif m == 'ProNE' or m == 'ProNE_prefactorization':
    #  return nodevectors.ProNE(n_components=K, save_svd=s, load_svd=l, svd_file=f)
    assert False, 'method (%s) should be one of: GGVec|GraRep|Glove|ProNE' % m

def output_embedding(G, E, outf):
    np.savez(outf, nodes=np.array(G.nodes()), edges=E)

#@profile
def do_file():

    #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)

    if not args.input_edge_list is None:
        # G = cg.read_edgelist(args.input, sep=args.delimiter, directed=False, quoting=3, prefix='X')
        G = cg.read_edgelist(args.input_edge_list, sep=args.delimiter, quoting=3, prefix='X')
        # model = nodevectors.GGVec()
    else:
        #print('# about to load graph: %0.2f' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

        import scipy.sparse
        # import nextworkx as nx
        M = scipy.sparse.load_npz(args.input_graph)

        #print('# transpose = %s: %0.2f' % (str(args.transpose), time.time() - t0), file=sys.stderr)

        if args.transpose:
            M = M.T

        #print('# about to convert to csr_matrix: %0.2f' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

        M = scipy.sparse.csr_matrix(M)
        # M2 = nx.from_scipy_sparse_matrix(M)

        #print('# enforcing symmetry: %0.2f' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()
        
        M += M.T

        #print('# about to convert to csrgraph: %0.2f' % (time.time() - t0), file=sys.stderr)
        sys.stderr.flush()

        G = cg.csrgraph(M)

    #print('# loading graph: %0.2f' % (time.time() - t0), file=sys.stderr)
    sys.stderr.flush()

    # I DON'T KNOW WHY, but this doesn't seem to work

    # About half of the time goes to pre_factorization
    # Thus, we can split the job into two pieces
    # This is important because the long queue has a limit on time
    if args.method == 'ProNE_prefactorization':
        #print('# method = %s, time: %0.2f' % (args.method, (time.time() - t0)), file=sys.stderr)
        m = method2model()
        features_matrix = m.pre_factorization(G.mat, m.n_components, m.exponent)
        #print('# pre_factorization time: %0.2f' % (time.time() - t0), file=sys.stderr)
        np.save(args.output + '.K' + str(args.components), features_matrix)
        return

    if args.features_matrix is None:
        embeddings = method2model().fit_transform(G)
    else: embeddings = method2model().fit_transform(G, features_matrix=np.load(args.features_matrix))

    #print('dict_to_embedding: # fitting model: %0.2f' % (time.time() - t0), file=sys.stderr)
    sys.stderr.flush()

    suffix = args.method + '.K' + str(args.components) + '.T' + str(args.threads) + '.O' + str(args.order) + '.w2v'
    prefix = strip_suffix(args.output, ['.txt', '.txt2'])
    outf = prefix + '.' +  suffix

    if not isinstance(embeddings, list):
        output_embedding(G, embeddings, outf)
    else:
        for i in range(len(embeddings)):
            output_embedding(G, embeddings[i], outf + '.' + str(i))

do_file()

#print('dict_to_embedding: # total time: %0.2f' % (time.time() - t0), file=sys.stderr)
