#!/usr/bin/env python

import sys,os,argparse,scipy,psutil
import numpy as np
import copy
from numpy import linalg as LA
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import KMeans,MiniBatchKMeans
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import metrics
import time
# node2vec
# from node2vec import Node2Vec
import networkx as nx
# for sparse matrix
from scipy import sparse
#early stop
from keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

print('GraphEncoder_clustering: ' + str(sys.argv), file=sys.stderr)

JSALTsrc=os.environ.get('JSALTsrc')

kwc_save_offset=0

t0 = time.time()                # added by kwc

# import numpy as np
# import argparse
# from sklearn.metrics.pairwise import cosine_similarity

# apikey=os.environ.get('SPECTER_API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--output", help="output file", required=True)
parser.add_argument("--save_prefix", help="output file", default=None)
parser.add_argument("-G", "--input_graph", help="input graph (readable by scipy.sparse.load_npz)", default=None)
parser.add_argument("-K", "--n_components", type=int, help="hidden dimensions [defaults = 32]", default=32)
parser.add_argument("--Laplacian", type=int, help="Laplacian [defaults = 1 (True)]", default=1)
parser.add_argument("--MaxIter", type=int, help="MaxIter [defaults = 50]", default=50)
parser.add_argument("--safe_mode", type=int, help="set to nonzero to be super careful", default=0)

# parser.add_argument("--search", help="query", action='store_true')
# parser.add_argument("--fields", help="comma separated fields", default='')
# parser.add_argument("--limit", type=int, help="max records to return", default=50)
# parser.add_argument("--debug", action='store_true')
# parser.add_argument("--citations", action='store_true')
# parser.add_argument("--recommendations", action='store_true')
# parser.add_argument("--batch", action='store_true')
args = parser.parse_args()

# Supress/hide the warning
# invalide devide resutls will be nan
np.seterr(divide='ignore', invalid='ignore')

############------------Auto_select_method_start-----------------###############
def Run(case, learn_opt, **kwargs):
  """
    input X can be a list of one of these format below:
    1. python list of n*n adjacency matrices.
    2. python list of s*2 edge lists.
    3. python list of s*3 edge lists.
    input Y can be these choices below:
    1. no Y input. The default will be [2,3,4,5] -- K range for clusters.
    2. n*1 class -- label vector. Positive labels are knwon labels and -1 indicate unknown labels.
    3. A range of potential number of clusters -- K (K clusters in total), i.e., [3, 4, 5].

    if input X is n*n adjacency =>  s*3 edg list
    if input X is s*2 => s*3 edg list

    Vertex size should be >10.

    Clustering / Classification
    The program automaticlly decide to run clustering or classification.
    1. If Y is a given cluster range, do clustering (case 1,3 for Y).
    2. If Y is a label vector (case 2 for Y), do classification.
    For classification: semi-supervised learning, supervised learning methods.
                        see the "Learner" defined below.


    Supervised learning "Learner":
      **Note the input trining set (X) need has fully known labels in Y.
      Learner = 1 run LDA, test on test set
      Learner = 0 run NN, test on test set

    Semi-supervised learning "Learner":
       **Note the input training set (X) need some unknown label(s) in Y.
      Learner=0 means embedding via known label, do not learn the unknown labels.
           Since only some nodes in the training set has known label,
           the test set is the unknwon labeled set, which is compared with
           the original labels of the unknown set
      Learner=1 means embedding via partial label, then learn unknown label via LDA.
        this runs semi-supervised learning with NN,
        the test will be on the result labels with the original labels

      Learner=2 means embedding via partial label, then learn unknown label via two-layer NN.
        this runs semi-supervised learning with NN,
        the test will be on the result labels with the original labels


  """

  defaultKwargs = {'Y':[2,3,4,5], 'DiagA': True,'Correlation': True,'Laplacian': args.Laplacian == 1,
                  'Learner': 1, 'LearnerIter': 0, 'MaxIter': 10, 'MaxIterK': 3,
                  'Replicates': 1, 'Attributes': False, 'neuron': 20, 'activation': 'relu',
                   'emb_opt': 'AEE', 'sparse_opt': 'None', 'Batch_input': False}
  kwargs = { **defaultKwargs, **kwargs }
  train_time = None # no seperate training time for semisuperviised learning yet
  total_begin = time.time()
  eval = Evaluation()
  kwargs_for_DataPreprocess =  {k: kwargs[k] for k in ['DiagA', 'Laplacian', 'Correlation', 'Attributes', 'emb_opt']}

  print('kwargs_for_DataPreprocess: ' + str(kwargs_for_DataPreprocess), file=sys.stderr) # added by kwc


  Dataset = DataPreprocess(case, **kwargs_for_DataPreprocess)

  print('DataPreposess done', file=sys.stderr) # added by kwc

  Y = case.Y
  n = case.n
  ari = None                    # added by kwc

  print('Y: ' + str(Y), file=sys.stderr) # added by kwc
  print('n: ' + str(Y), file=sys.stderr) # added by kwc

  # auto check block
  # if the option is not clustering, but the Y does not contain labels (known/unknwon) for n nodes.
  if (learn_opt != "c") and (len(Y) != n):
    learn_opt = "c" # do clustering
    print("The given Y do not have the same size as the node.Y is assumed as cluster number range.",
    "Clustering will be performed.",
    "If you want to do classification, stop the current run, reimport the Y with the right format then run again.",
    sep = "\n")

  # clustering
  if learn_opt == 'c':
    cluster = Clustering(Dataset)
    Z, Y, W, meanSS = cluster.cluster_main()
    if case.Y_ori is not None:
      ari = eval.clustering_test(Y, case.Y_ori)
      print("ARI: ", ari)
    else:
      ari = None

  # supervised learning
  if learn_opt == "su":
    Dataset = Dataset.supervise_preprocess()
    kwargs_for_learner = {k: kwargs[k] for k in ['Learner', 'LearnerIter', 'Batch_input']}
    train_strat = time.time()
    if kwargs['Learner'] == 1:
      lda = LDA(Dataset, **kwargs_for_learner)
      lda_res = lda.LDA_Learner(lda.DataSets)
      acc = eval.LDA_supervise_test(lda_res, Dataset.z_test, Dataset.Y_test)
    if kwargs['Learner'] == 0:
      gnn = GNN(Dataset, **kwargs_for_learner)
      gnn_res = gnn.GNN_complete()
      acc = eval.GNN_supervise_test(gnn_res, Dataset.z_test, Dataset.Y_test)
    train_end = time.time()
    train_time = train_end - train_strat
    print("acc: ", acc)

  # semisupervised learning
  if learn_opt == "se":
    Dataset = Dataset.semi_supervise_preprocess()
    kwargs_for_learner = {k: kwargs[k] for k in ['Learner', 'LearnerIter', 'Batch_input']}
    if kwargs['Learner'] == 2:
      gnn = GNN(Dataset, **kwargs_for_learner)
      gnn_res = gnn.GNN_complete()
      acc = eval.GNN_semi_supervised_learn_test(gnn_res.Y, case.Y_ori)
    if kwargs['Learner'] == 1:
      lda = LDA(Dataset, **kwargs_for_learner)
      lda_res = lda.LDA_Iter()
      acc = eval.GNN_semi_supervised_learn_test(lda_res.Y, case.Y_ori)
    if kwargs['Learner'] == 0:
      gnn = GNN(Dataset, **kwargs_for_learner)
      gnn_res = gnn.GNN_complete()
      acc = eval.GNN_semi_supervised_not_learn_test(gnn_res, Dataset, case)
    print("acc: ", acc)

  total_end = time.time()
  emb_time = Dataset.embed_time
  total_time = total_end - total_begin
  print("--- embed %s seconds ---" % emb_time)
  if train_time:
    print("--- train %s seconds ---" % train_time)
  print("--- total %s seconds ---" % total_time)

  if learn_opt != "c":
    Z_ori = Dataset.Z
    W_ori = Dataset.W

    sparse_opt = kwargs['sparse_opt']
    Z = To_single_sparse_matrix(Dataset.Z, sparse_opt)
    W = To_multi_sparse_matrix(Dataset.W, sparse_opt)

    return acc, train_time, emb_time, total_time, Z, W, Z_ori, W_ori

  else:
    return ari, train_time, emb_time, total_time, Z, W, Y

############------------node2vec_embed_start--------------------################
def node2vec_embed(X):
  G = nx.from_numpy_matrix(X)
  # use default setting from https://github.com/eliorc/node2vec
  node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4)
  # Embed nodes, use default setting from https://github.com/eliorc/node2vec
  model = node2vec.fit(window=2, min_count=1, batch_words=4)
  # get embedding matrix
  Z = model.wv.vectors
  return Z

############------------node2vec_embed_end----------------------################
############------------graph_encoder_embed_start----------------###############

def graph_encoder_embed(X,Y,n,**kwargs):
  if args.safe_mode > 0:
    Z_orig,W_orig = graph_encoder_embed_original(X,Y,n,**kwargs)
    Z_kwc,W_kwc = graph_encoder_embed_kwc(X,Y,n,**kwargs)
    Z_kwc2,W_kwc2 = graph_encoder_embed_kwc2(X,Y,n,**kwargs)

    # the two Zs and the two Ws should be very close to one another
    print('|Z_orig - Z_kwc| = ' + str(LA.norm(Z_orig - Z_kwc)), file=sys.stderr)
    print('|W_orig - W_kwc| = ' + str(LA.norm(W_orig - W_kwc)), file=sys.stderr)

    print('|Z_orig - Z_kwc2| = ' + str(LA.norm(Z_orig - Z_kwc2)), file=sys.stderr)
    print('|W_orig - W_kwc2| = ' + str(LA.norm(W_orig - W_kwc2)), file=sys.stderr)

    sys.stderr.flush()
    return Z_orig,W_orig
  else:
    return graph_encoder_embed_kwc2(X,Y,n,**kwargs)

def graph_encoder_embed_original(X,Y,n,**kwargs):
  """
    input X is s*3 edg list: nodei, nodej, connection weight(i,j)
    graph embedding function
  """
  global kwc_save_offset
  defaultKwargs = {'Correlation': True}
  kwargs = { **defaultKwargs, **kwargs}

  #If Y has more than one dimention , Y is the range of cluster size for a vertex. e.g. [2,10], [2,5,6]
  # check if Y is the possibility version. e.g.Y: n*k each row list the possibility for each class[0.9, 0.1, 0, ......]
  possibility_detected = False
  if Y.shape[1] > 1:
    k = Y.shape[1]
    possibility_detected = True
  else:
    # assign k to the max along the first column
    # Note for python, label Y starts from 0. Python index starts from 0. thus size k should be max + 1
    k = Y[:,0].max() + 1

  #nk: 1*n array, contains the number of observations in each class
  #W: encoder marix. W[i,k] = {1/nk if Yi==k, otherwise 0}
  nk = np.zeros((1,k))
  W = np.zeros((n,k))

  if possibility_detected:
    # sum Y (each row of Y is a vector of posibility for each class), then do element divid nk.
    nk=np.sum(Y, axis=0)
    W=Y/nk
  else:
    for i in range(k):
      nk[0,i] = np.count_nonzero(Y[:,0]==i)

    for i in range(Y.shape[0]):
      k_i = Y[i,0]
      if k_i >=0:
        W[i,k_i] = 1/nk[0,k_i]

  gee_t0 = time.time()          # added by kwc

  # Edge List Version in O(s)
  Z = np.zeros((n,k))

  print('possibility_detected: ' + str(possibility_detected), file=sys.stderr)
  print('Z.shape: ' + str(Z.shape), file=sys.stderr)
  print('X.shape: ' + str(X.shape), file=sys.stderr)
  print('Y.shape: ' + str(Y.shape), file=sys.stderr)

  print('X.dtype: ' + str(X.dtype), file=sys.stderr)

  # np.save('/tmp/X.npy', X)
  # np.save('/tmp/Y.npy', Y)
  # print('files saved', file=sys.stderr)
  # sys.stderr.flush()

  i = 0
  for row in X:
    [v_i, v_j, edg_i_j] = row
    v_i = int(v_i)
    v_j = int(v_j)
    if possibility_detected:
      for label_j in range(k):
        Z[v_i, label_j] = Z[v_i, label_j] + W[v_j, label_j]*edg_i_j
        if v_i != v_j:
          Z[v_j, label_j] = Z[v_j, label_j] + W[v_i, label_j]*edg_i_j
    else:
      label_i = Y[v_i][0]
      label_j = Y[v_j][0]

      if label_j >= 0:
        Z[v_i, label_j] = Z[v_i, label_j] + W[v_j, label_j]*edg_i_j
      if (label_i >= 0) and (v_i != v_j):
        Z[v_j, label_i] = Z[v_j, label_i] + W[v_i, label_i]*edg_i_j

  print('gee original: %0.3f; time so far: %0.3f' % (time.time() - gee_t0, time.time() - t0), file=sys.stderr) # added by kwc
  sys.stderr.flush()            # added by kwc

  Zpath = args.save_prefix + '.Z_orig.%d.f' % kwc_save_offset
  Z.astype(np.float32).tofile(Zpath)

  # Calculate each row's 2-norm (Euclidean distance).
  # e.g.row_x: [ele_i,ele_j,ele_k]. norm2 = sqr(sum(ele_i^2+ele_i^2+ele_i^2))
  # then divide each element by their row norm
  # e.g. [ele_i/norm2,ele_j/norm2,ele_k/norm2]
  if kwargs['Correlation']:
    row_norm = LA.norm(Z, axis = 1)
    reshape_row_norm = np.reshape(row_norm, (n,1))
    Z = np.nan_to_num(Z/reshape_row_norm)

  return Z, W



def kwc_save(Y, Z, W):
  global kwc_save_offset
  if args.safe_mode > 0 and args.save_prefix != None:
    np.save(args.save_prefix + '.Y.' + str(kwc_save_offset) + '.npy', Y)
    np.save(args.save_prefix + '.Z.' + str(kwc_save_offset) + '.npy', Z)
    np.save(args.save_prefix + '.W.' + str(kwc_save_offset) + '.npy', W)
  kwc_save_offset += 1

def maybe_save_X(X):
  global kwc_save_offset
  assert not args.save_prefix is None, '--save_prefix must be specified'

  if args.safe_mode > 0:
    X0path = args.save_prefix + '.X0.%d.i' % kwc_save_offset
    X1path = args.save_prefix + '.X1.%d.i' % kwc_save_offset
    X2path = args.save_prefix + '.X2.%d.f' % kwc_save_offset
    if os.path.exists(X0path):
      return X0path,X1path,X2path
  else:
    X0path = args.save_prefix + '.X0.i'
    X1path = args.save_prefix + '.X1.i'
    X2path = args.save_prefix + '.X2.f'

  X0 = X[:,0].astype(np.int32)
  X1 = X[:,1].astype(np.int32)
  X2 = X[:,2].astype(np.float32)

  X0.tofile(X0path)
  X1.tofile(X1path)
  X2.tofile(X2path)
  return X0path,X1path,X2path

def graph_encoder_embed_kwc2(X, Y,n,**kwargs):
  """
    input X is s*3 edg list: nodei, nodej, connection weight(i,j)
    graph embedding function
  """
  global kwc_save_offset
  defaultKwargs = {'Correlation': True}
  kwargs = { **defaultKwargs, **kwargs}

  kwc_gee_t0 = time.time()          # added by kwc
  
  X0path,X1path,X2path = maybe_save_X(X)

  #If Y has more than one dimention , Y is the range of cluster size for a vertex. e.g. [2,10], [2,5,6]
  # check if Y is the possibility version. e.g.Y: n*k each row list the possibility for each class[0.9, 0.1, 0, ......]

  # to simplify things, lets avoid more complicated cases
  if Y.shape[1] != 1: return None

  YY = Y.reshape(-1).astype(np.int32)
  Ypath = args.save_prefix + '.Y.%d.i' % kwc_save_offset
  Zpath = args.save_prefix + '.Z_kwc.%d.f' % kwc_save_offset
  YY.tofile(Ypath)

  # assign k to the max along the first column
  # Note for python, label Y starts from 0. Python index starts from 0. thus size k should be max + 1
  k = np.max(YY)+1

  #nk: 1*n array, contains the number of observations in each class
  #W: encoder matrix. W[i,k] = {1/nk if Yi==k, otherwise 0}
  nk = np.bincount(YY)
  nk2 = 1/nk.astype(np.float32)
  # nk2.to_file(args.save_prefix + '.nk2.f')

  W = scipy.sparse.csr_matrix((nk2[YY], (np.arange(len(YY)), YY)),
                              shape = (n,k), dtype=np.float32)

  # W = np.zeros((n,k))
  # for i, k_i in enumerate(YY):
  #     if k_i >=0:
  #       W[i,k_i] = nk2[k_i]

  # cmd = '%s/C/GEE %s.X0.i %s.X1.i %s.X2.f %s.Y.i > %s.Z.f' % (JSALTsrc, args.save_prefix, args.save_prefix, args.save_prefix, args.save_prefix, args.save_prefix)
  cmd = '%s/C/GEE %s %s %s %s > %s' % (JSALTsrc, X0path, X1path, X2path, Ypath, Zpath)
  print(cmd, file=sys.stderr)
  os.system(cmd)

  assert os.path.exists(Zpath), 'cmd failed'    

  Z = np.memmap(Zpath, dtype=np.float32, shape=(n, k), mode='r')

  # Calculate each row's 2-norm (Euclidean distance).
  # e.g.row_x: [ele_i,ele_j,ele_k]. norm2 = sqr(sum(ele_i^2+ele_i^2+ele_i^2))
  # then divide each element by their row norm
  # e.g. [ele_i/norm2,ele_j/norm2,ele_k/norm2]
  if kwargs['Correlation']:
    row_norm = LA.norm(Z, axis = 1)
    reshape_row_norm = np.reshape(row_norm, (n,1))
    Z = np.nan_to_num(Z/reshape_row_norm)

  kwc_save(YY, Z, W)

  print('gee kwc (plus time for saving): %0.3f; time so far: %0.3f; memory = %0.2f GBs' % (time.time() - kwc_gee_t0, time.time() - t0, psutil.Process().memory_info().rss / 1e9), file=sys.stderr) # added by kwc
  print(psutil.virtual_memory(), file=sys.stderr)
  sys.stderr.flush()            # added by kwc

  return Z, W


def graph_encoder_embed_kwc(X, Y,n,**kwargs):
  """
    input X is s*3 edg list: nodei, nodej, connection weight(i,j)
    graph embedding function
  """
  defaultKwargs = {'Correlation': True}
  kwargs = { **defaultKwargs, **kwargs}
  
  # maybe_save_X(X)

  #If Y has more than one dimention , Y is the range of cluster size for a vertex. e.g. [2,10], [2,5,6]
  # check if Y is the possibility version. e.g.Y: n*k each row list the possibility for each class[0.9, 0.1, 0, ......]

  # to simplify things, lets avoid more complicated cases
  if Y.shape[1] != 1: return None

  YY = Y.reshape(-1)
  # YY.tofile(args.save_prefix + '.Y.i')

  # assign k to the max along the first column
  # Note for python, label Y starts from 0. Python index starts from 0. thus size k should be max + 1
  k = np.max(YY)+1

  #nk: 1*n array, contains the number of observations in each class
  #W: encoder matrix. W[i,k] = {1/nk if Yi==k, otherwise 0}
  nk = np.bincount(YY)
  nk2 = 1/nk.astype(np.float32)
  # nk2.to_file(args.save_prefix + '.nk2.f')

  W = scipy.sparse.csr_matrix((nk2[YY], (np.arange(len(YY)), YY)),
                              shape = (n,k), dtype=np.float32)

  # W = np.zeros((n,k))
  # for i, k_i in enumerate(YY):
  #     if k_i >=0:
  #       W[i,k_i] = nk2[k_i]

  kwc_gee_t0 = time.time()          # added by kwc

  # os.system('%s/C/GEE %s.X0.i %s.X1.i %s.X2.f %s.Y.i > %s.Z.f' % (JSALTsrc, args.save_prefix, args.save_prefix, args.save_prefix, args.save_prefix, args.save_prefix))
  # Zfn = args.save_prefix + '.Z.f'
  # # Zlen = os.path.getsize(Zfn)
  # Z = np.memmap(Zfn, dtype=np.float32, shape=(n, k), mode='r')

  # Edge List Version in O(s)
  Z = np.zeros((n,k))

  # print('possibility_detected: ' + str(possibility_detected), file=sys.stderr)
  print('Z.shape: ' + str(Z.shape), file=sys.stderr)
  print('X.shape: ' + str(X.shape), file=sys.stderr)
  print('Y.shape: ' + str(Y.shape), file=sys.stderr)

  print('X.dtype: ' + str(X.dtype), file=sys.stderr)

  # np.save('/tmp/X.npy', X)
  # np.save('/tmp/Y.npy', Y)
  # print('files saved', file=sys.stderr)
  # sys.stderr.flush()

  X0 = X[:,0].astype(np.int32)
  X1 = X[:,1].astype(np.int32)
  X2 = X[:,2].astype(np.float32)

  for v_i, v_j, edg_i_j in zip(X0,X1,X2):
      label_i = YY[v_i]
      label_j = YY[v_j]

      if label_j >= 0:
        Z[v_i, label_j] += W[v_j, label_j]*edg_i_j
      if (label_i >= 0) and (v_i != v_j):
        Z[v_j, label_i] += W[v_i, label_i]*edg_i_j

  print('gee kwc: %0.3f; time so far: %0.3f' % (time.time() - kwc_gee_t0, time.time() - t0), file=sys.stderr) # added by kwc
  sys.stderr.flush()            # added by kwc

  # Calculate each row's 2-norm (Euclidean distance).
  # e.g.row_x: [ele_i,ele_j,ele_k]. norm2 = sqr(sum(ele_i^2+ele_i^2+ele_i^2))
  # then divide each element by their row norm
  # e.g. [ele_i/norm2,ele_j/norm2,ele_k/norm2]
  if kwargs['Correlation']:
    row_norm = LA.norm(Z, axis = 1)
    reshape_row_norm = np.reshape(row_norm, (n,1))
    Z = np.nan_to_num(Z/reshape_row_norm)

  # kwc_save(YY, Z, W)
  return Z, W


def multi_graph_encoder_embed(DataSets, Y, **kwargs):
  """
    input X contains a list of s3 edge list
    get Z and W by using graph emcode embedding
    Z is the concatenated embedding matrix from multiple graphs
    if there are attirbutes provided, add attributes to Z
    W is a list of weight matrix Wi
  """
  kwargs_single = {**kwargs}

  X = DataSets.X
  n = DataSets.n
  U = DataSets.U
  Graph_count = DataSets.Graph_count
  attributes = DataSets.attributes
  kwargs = DataSets.kwargs

  W = []

  for i in range(Graph_count):
      if i == 0:
          [Z, Wi] = graph_encoder_embed(X[i],Y,n,**kwargs_single)
      else:
          [Z_new, Wi] = graph_encoder_embed(X[i],Y,n,**kwargs)
          Z = np.concatenate((Z, Z_new), axis=1)
      W.append(Wi)

  # if there is attributes matrix U provided, add U
  if attributes:
    # add U to Z side by side
    Z = np.concatenate((Z, U), axis=1)

  return Z, W

############------------graph_encoder_embed_end------------------###############

############------------DataPreprocess_start---------------------###############
class DataPreprocess:
  def __init__(self, Dataset_input, **kwargs):
    self.kwargs = self.kwargs_construct(**kwargs)
    # Note, since every element in multi-graph list X has the same size and
    # node index, there will be only one column in Y for the node labels
    self.Y = Dataset_input.Y
    self.n = Dataset_input.n
    (self.X, self.Graph_count, self.embed_time) = self.input_prep(Dataset_input.X)
    (self.attributes, self.U) = self.check_attributes()
    self.Dataset_input = Dataset_input


  def kwargs_construct(self, **kwargs):
    defaultKwargs = {'DiagA': True,'Laplacian': False,  #input_prep
                     'Correlation': True,      # graph_encoder_embed
                     'Attributes': False,      # GNN_preprocess
                     }
    kwargs = { **defaultKwargs, **kwargs}  # update the args using input_args
    return kwargs


  def check_attributes(self):
    """
      return attributes detected flag and attributes U
    """
    kwargs = self.kwargs

    Attributes_detected = False
    U = None

    if kwargs["Attributes"]:
      U = kwargs["Attributes"]
      if U.shape[0] == n:
        Attributes_detected = True
    else:
        print("Attributes need to have the same size as the nodes.\
        If n nodes, need n rows")
    return Attributes_detected, U


  def test_edg_list_to_adj(self, n_test, n, edg_list):
    adj = np.zeros((n_test,n))

    for row in edg_list:
      [node_i, node_j, edge_i_j] = row
      adj[node_i, node_j] = edge_i_j

    return adj


  def input_prep(self, X):
    kwargs = self.kwargs
    # if X is a single numpy object, put this numpy object in a list
    if type(X) == np.ndarray:
      X = [X]

    ## Now X is a list of numpy objects
    # each element can be a numpy object for adjacency matrix or edge list
    Graph_count = len(X)

    # AEE needs X to be a list of edge list
    if kwargs["emb_opt"] == "AEE":
      X, embed_time = self.input_prep_AEE(X, Graph_count)
    # Node2Vec only needs a list of adjacency matrix
    if kwargs["emb_opt"] == "Node2Vec":
      embed_time = 0
      pass

    return X, Graph_count, embed_time


  def input_prep_AEE(self, X, Graph_count):
    """
      X may be a single numpy object or a list of numpy objects
      The multi-graph input X is assumed has the same node numbers
      for each element in X, and the node are indexed the same way
      amonge the elements. e.g. node_0 in X[1] is the same node_0 in X[2].
      return X as a list of s*3 edge lists
      return n, which is the total number of nodes
    """

    # need total labeled number n
    # if try to get from the edg list, it may miss the node that has no connection with others but has label
    n = self.n

    embed_time = 0
    for i in range(Graph_count):
      X_tmp = X[i]
      X_tmp = self.to_s3_list(X_tmp)

      # count the time for laplacian and diagnal only
      embed_begin = time.time()
      X_tmp = self.single_X_prep(X_tmp, n)
      embed_end = time.time()
      embed_time += (embed_end - embed_begin)

      X[i] = X_tmp

    return X, embed_time


  def to_s3_list(self,X):
    """
      the input X is a single graph, can be adjacency matrix or edgelist
      this function will return a s3 edge list
    """
    (s,t) = X.shape

    if s == t:
      # convert adjacency matrix to edgelist
      X = self.adj_to_edg(X);
    else:
      # for either s*2 or s*3 case, calculate n -- vertex number
      if t == 2:
        # enlarge the edgelist to s*3 by adding 1 to the thrid position as adj(i,j)
        # X = np.insert(X, 1, np.ones(s,1))
        X = np.insert(X, 1, np.ones((s,1))) # modified by kwc

    return X


  def single_X_prep(self, X, n):
    """
      input X is a single S3 edge list
      this adds Diagnal augement and Laplacian normalization to the edge list
    """
    kwargs = self.kwargs

    X = X.astype(np.float32)

    # Diagnal augment
    if kwargs['DiagA']:
      # add self-loop to edg list -- add 1 connection for each (i,i)
      self_loops = np.column_stack((np.arange(n), np.arange(n), np.ones(n)))
      # faster than vstack --  adding the second to the bottom
      X = np.concatenate((X,self_loops), axis = 0)

    # Laplacian
    s = X.shape[0] # get the row number of the edg list
    if kwargs["Laplacian"]:
      D = np.zeros((n,1))
      for row in X:
        [v_i, v_j, edg_i_j] = row
        v_i = int(v_i)
        v_j = int(v_j)
        D[v_i] = D[v_i] + edg_i_j
        if v_i != v_j:
          D[v_j] = D[v_j] + edg_i_j

      D = np.power(D, -0.5)

      for i in range(s):
        X[i,2] = X[i,2] * D[int(X[i,0])] * D[int(X[i,1])]

    return X


  def adj_to_edg(self,A):
    """
      input is the symmetric adjacency matrix: A
      other variables in this function:
      s: number of edges
      return edg_list -- matrix format with shape(edg_sum,3):
      example row in edg_list(matrix): [vertex1, vertex2, connection weight from Adj matrix]
    """
    # check the len of the second dimenson of A
    if A.shape[1] <= 3:
      edg = A
    else:
      n = A.shape[0]
      # construct the initial edgg_list matrix with the size of (edg_sum, 3)
      edg_list = []
      for i in range(n):
        for j in range(i, n):
          if A[i,j] > 0:
            row = [i, j, A[i,j]]
            edg_list.append(row)
      edg = np.array(edg_list)
    return edg


  def semi_supervise_preprocess(self):
    """
      get Z, W using multi_graph_encoder_embed()
      get training sets and testing sets for Z and Y by using split_data()

    """
    DataSets =  copy.deepcopy(self)
    Y = DataSets.Y
    kwargs = DataSets.kwargs
    Encoder_kwargs = {k: kwargs[k] for k in ['Correlation']}
    # semisupervise do embedding during the learning process
    # this timer is only for the first embedding for the normalized input X
    embed_time_main_begin = time.time()
    if kwargs["emb_opt"] == "AEE":
      (DataSets.Z, DataSets.W) = multi_graph_encoder_embed(DataSets, Y, **Encoder_kwargs)
    if kwargs["emb_opt"] == "Node2Vec":
      DataSets.Z = node2vec_embed(DataSets.X)

    embed_time_main_end = time.time()
    embed_time_main = embed_time_main_end - embed_time_main_begin

    DataSets.k = DataSets.get_k()
    DataSets = DataSets.split_data()
    DataSets.embed_time = DataSets.embed_time + embed_time_main

    return DataSets


  def get_k(self):
    Y = self.Y
    n = self.n
    # get class number k or the largest cluster size
    # max of all flattened element + 1
    if len(Y) == n:
      k = np.amax(Y) + 1
    return k


  def split_data(self):
    split_Sets =  copy.deepcopy(self)

    Y = split_Sets.Y
    Z = split_Sets.Z

    ind_train = np.argwhere (Y >= 0)[:,0]
    ind_unlabel = np.argwhere (Y < 0)[:,0]

    Y_train = Y[ind_train, 0]
    z_train = Z[ind_train]

    Y_unlabel = None
    z_unlabel = None

    if len(ind_unlabel) > 0:
      Y_unlabel = Y[ind_unlabel, 0]
      z_unlabel = Z[ind_unlabel]

    # Convert targets into one-hot encoded format
    Y_train_one_hot = to_categorical(Y_train)

    split_Sets.ind_unlabel = ind_unlabel
    split_Sets.ind_train = ind_train
    split_Sets.Y_train = Y_train
    split_Sets.Y_unlabel = Y_unlabel
    split_Sets.z_train = z_train
    split_Sets.z_unlabel = z_unlabel
    split_Sets.Y_train_one_hot = Y_train_one_hot

    return split_Sets


  def DataSets_reset(self, option):
    """
      based on the information of the given new Y:
      1. reassign Z and W to the given DataSets,
      2. update z_train, z_unlabel
      Input Option:
      1. if the option is "y_temp", do graph encoder using y_temp
    """
    NewSets =  copy.deepcopy(self)
    kwargs = NewSets.kwargs
    ind_unlabel = NewSets.ind_unlabel
    ind_train = NewSets.ind_train
    y_temp =  NewSets.y_temp
    Encoder_kwargs = {k: kwargs[k] for k in ['Correlation']}

    # different versions
    if option == "y_temp":
      [Z,W] = multi_graph_encoder_embed(NewSets, y_temp, **Encoder_kwargs)
    if option == "y_temp_one_hot":
      y_temp_one_hot = NewSets.y_temp_one_hot
      [Z,W] = multi_graph_encoder_embed(NewSets, y_temp_one_hot, **Encoder_kwargs)
    if NewSets.attributes:
      # add U to Z side by side
      Z = np.concatenate((Z, NewSets.U), axis=1)

    NewSets.Z = Z
    NewSets.W = W
    NewSets.z_train = Z[ind_train]
    NewSets.z_unlabel = Z[ind_unlabel]

    return NewSets


  def supervise_preprocess(self):
    """
      adding test sets for supervised learning
      this function assumes only one test set
      if there is a list of test set, needs to modify this function
    """

    DataSets = self.semi_supervise_preprocess()
    Dataset_input = DataSets.Dataset_input

    DataSets.z_test = DataSets.Z[Dataset_input.test_idx]
    DataSets.Y_test = Dataset_input.Y_test.ravel()
    DataSets.z_unlabel = None
    DataSets.Y_unlabel = None

    return DataSets
############------------DataPreprocess_end-----------------------###############

############-----------------GNN_start---------------------------###############
def batch_generator(X, y, k, batch_size, shuffle):
    number_of_batches = int(X.shape[0]/batch_size)
    counter = 0
    sample_index = np.arange(X.shape[0])
    if shuffle:
        np.random.shuffle(sample_index)
    while True:
        batch_index = sample_index[batch_size*counter:batch_size*(counter+1)]
        X_batch = X[batch_index,:]
        y_batch = y[batch_index,:]
        counter += 1
        yield X_batch, y_batch
        if (counter == number_of_batches):
            if shuffle:
                np.random.shuffle(sample_index)
            counter = 0

class Hyperperameters:
  """
    define perameters for GNN.
    default values are for GNN learning -- "Leaner" ==2:
      embedding via partial label, then learn unknown label via two-layer NN

  """
  def __init__(self):
    # there is no scaled conjugate gradiant in keras optimiser, use defualt instead
    # use whatever default
    self.learning_rate = 0.01  # Initial learning rate.
    self.epochs = 100 #Number of epochs to train.
    self.hidden = 20 #Number of units in hidden layer
    self.val_split = 0.1 #Split 10% of training data for validation
    self.loss = 'categorical_crossentropy' # loss function


class GNN:
  def __init__(self, DataSets, **kwargs):
    GNN.kwargs = self.kwargs_construct(**kwargs)
    GNN.DataSets = DataSets
    GNN.hyperM = Hyperperameters()
    GNN.model = self.GNN_model()  #model summary: GNN.model.summary()
    GNN.meanSS = 0  # initialize the self-defined critirion meanSS

  def kwargs_construct(self, **kwargs):
    defaultKwargs = {'Learner': 1,                    # GNN_Leaner
                     'LearnerIter': 0,                # GNN_complete, GNN_Iter
                     "Replicates": 3,                 # GNN_Iter
                     "Batch_input": False              # if run in batches
                     }
    kwargs = { **defaultKwargs, **kwargs}  # update the args using input_args
    return kwargs


  def GNN_model(self):
    """
      build GNN model
    """
    hyperM = self.hyperM
    DataSets = self.DataSets

    z_train = DataSets.z_train
    k = DataSets.k

    feature_num = z_train.shape[1]

    model = keras.Sequential([
    keras.layers.Flatten(input_shape = (feature_num,)),  # input layer
    keras.layers.Dense(hyperM.hidden, activation='relu'),  # hidden layer -- no tansig activation function in Keras, use relu instead
    keras.layers.Dense(k, activation='softmax') # output layer, matlab used softmax for patternnet default ??? max(opts.neuron,K)? opts
    ])

    optimizer = keras.optimizers.Adam(learning_rate = hyperM.learning_rate)

    model.compile(optimizer='adam',
                  loss=hyperM.loss,
                  metrics=['accuracy'])

    return model


  def GNN_run(self, k, z_train, y_train_one_hot, z_unlabel):
    """
      Train and test directly.
      Do not learn from the unknown labels.
    """
    gnn = copy.deepcopy(self)
    hyperM = gnn.hyperM
    model = gnn.model
    batch_flag = self.kwargs["Batch_input"]

    if batch_flag:
      early_stopping_callback = EarlyStopping(monitor='loss', patience=5, verbose=0)
      checkpoint_callback = ModelCheckpoint('GNN.h5', monitor='loss', save_best_only=True, mode='min', verbose=0)

      history = model.fit(batch_generator(z_train, y_train_one_hot, k, 32, True),
                      epochs=hyperM.epochs,
                      steps_per_epoch=z_train.shape[0],
                      callbacks=[early_stopping_callback, checkpoint_callback],
                      verbose=0)
    else:
      # validation_split=hyperM.val_split
      history = model.fit(z_train, y_train_one_hot,
            validation_split=hyperM.val_split,
            epochs=hyperM.epochs,
            shuffle=True,
            verbose=0)

    train_acc = history.history['accuracy'][-1]

    predict_probs = None
    pred_class = None
    pred_class_prob = None
    if type(z_unlabel) == np.ndarray:
      # predict_probas include probabilities for all classes for each node
      predict_probs = model.predict(z_unlabel)
      # assign the classes with the highest probability
      pred_class = np.argmax(predict_probs, axis=1)
      # the corresponding probabilities of the predicted classes
      pred_class_prob = predict_probs[range(len(predict_probs)),pred_class]

    gnn.model = model
    gnn.train_acc = train_acc
    gnn.pred_probs = predict_probs
    gnn.pred_class = pred_class
    gnn.pred_class_prob = pred_class_prob


    return gnn

  def GNN_Direct(self, DataSets, y_train_one_hot):
    """
      This function can run:
      1. by itself, when interation is set to False (<1)
      2. inside GNN_Iter, when interation is set to True (>=1)

      Learner == 0: GNN, but not learn from the known label
      Learner == 2: GNN, and learn unknown labels
    """
    Learner = self.kwargs["Learner"]

    k = DataSets.k
    z_train = DataSets.z_train
    Y = DataSets.Y
    z_unlabel = DataSets.z_unlabel
    ind_unlabel = DataSets.ind_unlabel

    gnn = self.GNN_run(k, z_train, y_train_one_hot, z_unlabel)

    if Learner == 0:
      # do not learn unknown label.
      pass

    if Learner == 2:
      # learn unknown label based on the known label
      # replace the unknown label in Y with predicted labels
      pred_class = gnn.pred_class
      Y[ind_unlabel, 0] = pred_class

    gnn.Y = Y

    return gnn


  def GNN_Iter(self, DataSets):
    """
      Run this function when interation is set, which is >=1.

      1. randomly assign labels to the unknown labels, get Y_temp
      2. get Y_one_hot for the Y_temp
      3. get Z from graph_encod function with X and Y_temp
      within each loop:
        use meanSS as its criterion to decide if the update is needed
          update Y_one_hot for the unknown labels with predict probabilities of each classes
          update Y with the highest possible predicted labels
          update z_train and z_unlabel from graph encoder embedding using the updated Y
          train the model with the updated z_train and Y_one_hot
    """

    kwargs = self.kwargs
    meanSS = self.meanSS

    k = DataSets.k
    Y = DataSets.Y
    ind_unlabel = DataSets.ind_unlabel


    y_temp = np.copy(Y)
    DataSets.y_temp = y_temp


    for i in range(kwargs["Replicates"]):
      # assign random integers in [1,K] to unassigned labels
      r = [i for i in range(k)]

      ran_int = np.random.choice(r, size=(len(ind_unlabel),1))

      y_temp[ind_unlabel] = ran_int

      for j in range(kwargs["LearnerIter"]):
        if j ==0:
          # first iteration need to split the y_temp for training etc.
          # use reset to add z_train, z_unlabel, y_temp_one_hot, to the dataset
          DataSets = DataSets.DataSets_reset("y_temp")
          # Convert targets into one-hot encoded format
          y_temp_one_hot = to_categorical(y_temp)
          # initialize y_temp_one_hot in the first loop
          DataSets.y_temp_one_hot = y_temp_one_hot
        if j > 0:
          # update z_train, z_unlabel, and y_temp_train_one_hot to the dataset
          DataSets = DataSets.DataSets_reset("y_temp")
        # all the gnn train on y_train_one_hot
        gnn = self.GNN_Direct(DataSets, DataSets.Y_train_one_hot)
        predict_probs = gnn.pred_probs
        pred_class = gnn.pred_class
        pred_class_prob = gnn.pred_class_prob

        # z_unknown is initialized with none, so the pred_class may be none
        # This will not happen for the semi version,
        # since the unknown size should not be none for the semi version
        if type(pred_class) == np.ndarray:
          # if there are unkown labels and predicted labels are available
          # check if predicted_class are the same as the random integers
          # if so, stop the iteration in "LearnerIter" loop
          # shape (n,) is required for adjusted_rand_score()
          if adjusted_rand_score(ran_int.reshape((-1,)), pred_class) == 1:
            break
          # assign the probabilites for each class to the temp y_one_hot
          DataSets.y_temp_one_hot[ind_unlabel] = predict_probs
          # assgin the predicted classes to the temp Y unknown labels
          DataSets.y_temp[ind_unlabel, 0] = pred_class
          # # assign the highest possibility of the class to Y_temp
          # Y_temp[ind_unlabel, 0] = pred_class_prob
      minP = np.mean(pred_class_prob) - 3*np.std(pred_class_prob)
      if minP > meanSS:
        meanSS = minP
        Y = DataSets.y_temp

      gnn.Y = Y
      gnn.meanSS = meanSS
      return gnn


  def GNN_complete(self):
    """
      if LearnerIter set to False(<1):
        run GNN_Direct() with no iteration
      if LearnerIter set to True(>=1):
        run GNN_Iter(), which starts with radomly assigned k to unknown labels

    """
    kwargs = self.kwargs

    DataSets = self.DataSets
    y_train = DataSets.Y_train


    if kwargs["LearnerIter"] < 1:
      # Convert targets into one-hot encoded format
      y_train_one_hot = to_categorical(y_train)
      gnn = self.GNN_Direct(DataSets, y_train_one_hot)
    else:
      gnn = self.GNN_Iter(DataSets)

    return gnn
############-----------------GNN_end-----------------------------###############

############-----------------LDA_start---------------------------###############
class LDA:
  def __init__(self, DataSets, **kwargs):
    LDA.kwargs = self.kwargs_construct(**kwargs)
    LDA.DataSets = DataSets
    LDA.model = LinearDiscriminantAnalysis()  # asssume spseudolinear is its default setting
    LDA.meanSS = 0  # initialize the self-defined critirion meanSS

  def kwargs_construct(self, **kwargs):
    defaultKwargs = {'Learner': 1,                         # LDA_Leaner
                     'LearnerIter': 0, "Replicates": 3     # LDA_Iter
                     }
    kwargs = { **defaultKwargs, **kwargs}  # update the args using input_args
    return kwargs

  def LDA_Learner(self, DataSets):
    """
      run this function when Learner set to 1.
      embedding via partial label, then learn unknown label via LDA.
    """
    lda = copy.deepcopy(self)
    z_train = DataSets.z_train
    y_train = DataSets.Y_train
    ind_unlabel = DataSets.ind_unlabel
    z_unlabel = DataSets.z_unlabel
    Y = DataSets.Y

    model = self.model
    model.fit(z_train,y_train)
    # train_acc = model.score(z_train,y_train)

    # for semi-supervised learning
    if type(z_unlabel) == np.ndarray:
      # predict_probas include probabilities for all classes for each node
      pred_probs = model.predict_proba(z_unlabel)
      # assign the classes with the highest probability
      pred_class = model.predict(z_unlabel)
      # the corresponding probabilities of the predicted classes
      pred_class_prob = pred_probs[range(len(pred_probs)),pred_class]
      # assign the predicted class to Y
      Y[ind_unlabel, 0] = pred_class
      lda.Y = Y
      lda.pred_class = pred_class
      lda.pred_class_prob = pred_class_prob

    lda.model = model
    return lda

  def LDA_Iter(self):
    """
      run this function when Learner set to 1, and LeanerIter is True(>=1)
      ramdonly assign labels to the unknownlabel.
      embedding via partial label, then learn unknown label via LDA.
    """

    kwargs = self.kwargs
    meanSS = self.meanSS
    DataSets = self.DataSets

    k = DataSets.k
    Y = DataSets.Y
    ind_unlabel = DataSets.ind_unlabel

    y_temp = np.copy(Y)

    for i in range(kwargs["Replicates"]):
      # assign random integers in [1,K] to unassigned labels
      r = [i for i in range(k)]

      ran_int = np.random.choice(r, size=(len(ind_unlabel),1))

      y_temp[ind_unlabel] = ran_int

      DataSets.y_temp = y_temp

      for j in range(kwargs["LearnerIter"]):
        # use reset to add z_train, z_unlabel, to the dataset
        DataSets = DataSets.DataSets_reset("y_temp")
        # all train on y_train
        lda = self.LDA_Learner(DataSets)
        pred_class = lda.pred_class
        pred_class_prob = lda.pred_class_prob

        # z_unknown is initialized with none, so the pred_class may be none
        # This will not happen for the semi version,
        # since the unknown size should not be none for the semi version
        if type(pred_class) == np.ndarray:
          # if there are unkown labels and predicted labels are available
          # check if predicted_class are the same as the random integers
          # if so, stop the iteration in "LearnerIter" loop
          # shape (n,) is required for adjusted_rand_score()
          if adjusted_rand_score(ran_int.reshape((-1,)), pred_class) == 1:
            break
          # assgin the predicted classes to the temp Y unknown labels
          DataSets.y_temp[ind_unlabel, 0] = pred_class
          # # assign the highest possibility of the class to Y_temp
          # Y_temp[ind_unlabel, 0] = pred_class_prob
      minP = np.mean(pred_class_prob) - 3*np.std(pred_class_prob)
      if minP > meanSS:
        meanSS = minP
        Y = DataSets.y_temp

      lda.Y = Y
      lda.meanSS = meanSS
      return lda


############-----------------LDA_end-----------------------------###############

############------------Clustering_start-------------------------###############
class Clustering:
  """
    The input DataSets.X is the s*3 edg list
    The innput DataSets.Y can be:
    1. A given cluster size, e.g. [3], meaning in total 3 clusters
    2. A range of cluster sizes. e.g. [3-5], meaning there are possibly 3 to 5 clusters

  """
  def __init__(self, DataSets, **kwargs):
    self.kwargs = self.kwargs_construct(**kwargs)
    self.DataSets = DataSets
    self.cluster_size_range = self.cluster_size_check()
    self.K = DataSets.Y[0]


  def kwargs_construct(self, **kwargs):
    defaultKwargs = {'Correlation': True,'MaxIter': args.MaxIter, 'MaxIterK': 5,'Replicates': 3}
    kwargs = { **defaultKwargs, **kwargs}
    return kwargs

  def cluster_size_check(self):
    DataSets = self.DataSets
    Y = DataSets.Y

    cluster_size_range = None # in case that Y is an empty array.

    if len(Y) == 1:
      cluster_size_range = False  # meaning the cluster size is known. e.g. [3]
    if len(Y) > 1:
      cluster_size_range = True   # meaning only know the range of cluster size. e.g. [2, 3, 4, 5]

    return cluster_size_range

  def graph_encoder_cluster(self, K):
    """
      clustering function
    """
    DataSets = self.DataSets
    X = DataSets.X
    n = DataSets.n
    kwargs = self.kwargs
    Encoder_kwargs = {k: kwargs[k] for k in ['Correlation']}

    print('calling graph_encoded_cluster: ' + str(kwargs), file=sys.stderr) # added by kwc

    minSS=-1
    Z = None
    W = None

    for i in range(kwargs['Replicates']):
      Y_temp = np.random.randint(K,size=(n,1))
      print('i: %d, %0.3f sec' %(i, time.time() - t0), file=sys.stderr) # added by kwc
      for r in range(kwargs['MaxIter']):
        print('r: %d (of %d), %0.3f sec' % (r, kwargs['MaxIter'], time.time() - t0), file=sys.stderr) # added by kwc
        sys.stderr.flush()

        multi_graph_encoder_t0 = time.time()
        [Zt,Wt] = multi_graph_encoder_embed(DataSets, Y_temp, **Encoder_kwargs)
        print('multi_graph_encoder with K = %d, replica: %d, iteration: %d, took %0.3f sec; time so far: %0.3f sec' % (K, i, r, time.time() - multi_graph_encoder_t0, time.time() - t0), file=sys.stderr)  # added by kwc
        sys.stderr.flush()

        if DataSets.attributes:
          # add U to Z side by side
          Zt = np.concatenate((Zt, DataSets.U), axis=1)

        kmeans_t0 = time.time()
        # kmeans = KMeans(n_clusters=K, max_iter = kwargs['MaxIter']).fit(Zt)
        kmeans = MiniBatchKMeans(n_clusters=K, max_iter = kwargs['MaxIter']).fit(Zt)

        print('MiniBatchKMeans with K = %d, replica: %d, iteration: %d, took %0.3f sec; time so far: %0.3f sec; memory = %0.2f GBs' % (K, i, r, time.time() - kmeans_t0, time.time() - t0, psutil.Process().memory_info().rss /1e9), file=sys.stderr)  # added by kwc
        print(psutil.virtual_memory(), file=sys.stderr)
        sys.stderr.flush()

        labels = kmeans.labels_ # shape(n,)
        # sum_in_cluster = kmeans.inertia_ # sum of distance within cluster (k,1)

        transform_t0 = time.time() # added by kwc
        dis_to_centors = kmeans.transform(Zt)
        print('kmeans.transform with K = %d, replica: %d, iteration: %d, took %0.3f sec; time so far: %0.3f sec' % (K, i, r, time.time() - transform_t0, time.time() - t0), file=sys.stderr)  # added by kwc
        sys.stderr.flush()

        # adjusted_rand_score() needs the shape (n,)
        if adjusted_rand_score(Y_temp.reshape(-1,), labels) == 1:
          break
        else:
          # we need labels to be the same shape as for Y(n,1) when assign
          Y_temp = labels.reshape(-1,1)

      # calculate score and compare with meanSS
      tmp = self.temp_score(dis_to_centors, K, labels, n)
      if (minSS == -1) or tmp < minSS:
        Z = Zt
        W = Wt
        minSS = tmp
        Y = labels

    print('leaving graph_encoded_cluster', file=sys.stderr)  # added by kwc
    return  Z, Y, W, minSS


  def temp_score(self, dis_to_centors, K, labels, n):
    """
      calculate:
      1. sum_in_cluster(1*k): the sum of the distance from the nodes to the centroid
      of its belonged cluster
      2. sum_in_cluster_norm(1*k): normalize the sum_in_cluster by the
      corresponding label count (how many nodes in each cluster)
      3. sum_not_in_cluster(1*k): the sum of the distance of the cluster
      centroid to the nodes that do not belong to the cluster
      4. sum_not_in_cluster_norm(1*k): normalize the sum_other_centroids by the
      counts of the nodes that do not belong to the cluster.
      5. temp score(1*k):
      (normalized sum in cluster / normalized sum not in cluster ) *
      (label count in cluster / total node number)
      6. get mean + 2 standard deviation of temp score, then return
    """
    label_count = np.bincount(labels)
    sum_in_cluster_squre = np.zeros((K,))

    dis_to_centors_squre = dis_to_centors**2

    for i in range(n):
      label = labels[i]
      sum_in_cluster_squre[label] += dis_to_centors_squre[i][label]

    # how to find out if the distance is squared, the current method doesn't do square root.
    sum_not_in_cluster = (np.sum(dis_to_centors_squre, axis=0) - sum_in_cluster_squre)**0.5

    sum_not_in_cluster_norm = sum_not_in_cluster/(n - label_count)
    sum_in_cluster_norm = sum_in_cluster_squre**0.5/label_count

    tmp = sum_in_cluster_norm / sum_not_in_cluster_norm * label_count / n
    tmp = np.mean(tmp) + 2*np.std(tmp)

    return tmp


  def cluster_main(self):
    K = self.K
    DataSets = self.DataSets
    X = DataSets.X
    n = DataSets.n

    kmax = np.amax(K)
    if n/kmax < 30:
      print('Too many clusters at maximum. Result may bias towards large K. Please make sure n/Kmax >30.')
    # when the cluster size is specified
    if not self.cluster_size_range:
      [Z,Y,W,meanSS]= self.graph_encoder_cluster(K[0])
    # when the range of cluster size is provided
    # columns are less than n/2 and kmax is less than max(n/2, 10)
    if self.cluster_size_range:
      k_range = len(K)
      if k_range < n/2 and kmax < max(n/2, 10):
          minSS = -1
          Z = 0
          W = 0
          meanSS = np.zeros((k_range,1))
          for i in range(k_range):
            [Zt,Yt,Wt,tmp]= self.graph_encoder_cluster(K[i])
            meanSS[i,0] = i
            if (minSS == -1) or tmp < minSS:
              minSS = tmp
              Y = Yt
              Z = Zt
              W = Wt
    return Z, Y, W, meanSS

############------------Clustering_end---------------------------###############
############------------Evaluation_start---------------------------#############
class Evaluation:
  def GNN_supervise_test(self, gnn, z_test, y_test):
    """
      test the accuracy for GNN_direct
    """
    y_test_one_hot = to_categorical(y_test)
    # set verbose to 0 to silent the output
    test_loss, test_acc = gnn.model.evaluate(z_test,  y_test_one_hot, verbose=0)

    return test_acc

  def LDA_supervise_test(self, lda, z_test, y_test):
    """
      test the accuracy for LDA_learner
    """
    test_acc = lda.model.score(z_test, y_test)

    return test_acc

  def GNN_semi_supervised_learn_test(self,Y_result, Y_original):
    """
      test accuracy for semi-supervised learning
    """
    test_acc = metrics.accuracy_score(Y_result, Y_original)

    return test_acc

  def GNN_semi_supervised_not_learn_test(self, gnn, Dataset, case):
    """
      test accuracy for semi-supervised learning
    """

    ind_unlabel = Dataset.ind_unlabel
    z_unlabel =  Dataset.z_unlabel
    y_unlabel_ori = case.Y_ori[ind_unlabel, 0]
    y_unlabel_ori_one_hot = to_categorical(y_unlabel_ori)
    test_loss, test_acc = gnn.model.evaluate(z_unlabel, y_unlabel_ori_one_hot, verbose=0)

    return test_acc


  def clustering_test(self, Y_result, Y_original):
    """
      test accuracy for semi-supervised learning
    """
    ari = adjusted_rand_score(Y_result, Y_original.reshape(-1,))

    return ari

############-----------------Matrix_conversion-------------------###############
def To_multi_sparse_matrix(M_list,option):
  M_list_new = []
  for M in M_list:
    M_new = To_single_sparse_matrix(M,option)
    M_list_new.append(M_new)

  return M_list_new

def To_single_sparse_matrix(M,option):
  """
    coo_matrix is efficient and fast to construct,
      However, arithmetic operations are not efficient on this matrix.
      One can easily convert coo_matrix to csc_matrix/csr_matrix
    csc_matrix/csr_matrix are efficient in column_slicing/row_slicing,
      One can have efficient multiplication or inversion.
  """
  if option == "coo":
    M = sparse.coo_matrix(M)
  if option == "csr":
    M = sparse.csr_matrix(M)
  if option == "csc":
    M = sparse.csc_matrix(M)

  return M


class TestCase:
  def __init__(self, n, X, Y, Y_ori):
    """
      Initialize the class
      n: the number of nodes
      X: initialize the adjacency matrix or edge list
      Y: initialize the classes
    """
    self.n = n
    self.X = X
    self.Y = Y        # if want 3 clusters, make it a np array: [[3]], see example below
    self.Y_ori = Y_ori    # if you know the cluster info, put in here for evaluation

## load the data. G should either be n*n sparse matrix, or s*2 edgelist
from scipy.sparse import load_npz
G=load_npz(args.input_graph)

# n=4294967295 ## number of vertices / maximum id in G
nz = G.nonzero()

n = 1+ max(np.max(nz[0]),np.max(nz[1]))

D=[[args.n_components]] ## default embedding dimension.
# testCase = TestCase(n, G, D, None)
nz2 = np.array([nz[0], nz[1], np.ones(len(nz[0]))]).T
print('nz2.shape: ' + str(nz2.shape), file=sys.stderr)

testCase = TestCase(n, nz2, D, None)

import warnings
warnings.filterwarnings("ignore")
ari, train_time, emb_time, total_time, Z, W, Y = Run(testCase, "c")

"""
final embedding: Z
estimated Cluster label: Y
running time: total_time
"""

print('train_time: ' + str(train_time), file=sys.stderr)
print('emb_time: ' + str(emb_time), file=sys.stderr)
print('total_time: ' + str(total_time), file=sys.stderr)

np.save(args.output, Z)

print('done, %0.3f sec' % (time.time() - t0), file=sys.stderr)  # added by kwc
