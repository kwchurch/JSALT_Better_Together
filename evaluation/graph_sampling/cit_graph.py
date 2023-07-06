import scipy, numpy as np, os

if __name__ == '__main__':

	
	citation_graph = os.path.join(os.environ['JSALTdir'], 'semantic_scholar/releases/2022-12-02/database/citations/graphs/citations.G.npz')
	print(f'Loading citation graph from {citation_graph}')
	M = scipy.sparse.load_npz(citation_graph)
	
	id_to_bin = os.path.join(os.environ['JSALTdir'], 'semantic_scholar/j.ortega/id_to_bin.tsv')
	print(f'Load id2bin from {id_to_bin}')
	#>> paste classes.txt corp_by_date_nonullyear_with_int.tsv.kwc.V4 | awk 'BEGIN{OFS="\t"} {print $2,$1}' > id_to_bin.tsv
	bin_matrix = np.loadtxt(id_to_bin, dtype='int32')
	
	num_out_edges = np.asarray(np.sum(M, axis=1)).squeeze() # Shape 270 000 000 x 1 ; np.array(num_out_edges).reshape(-1)
	
	x,y = M.nonzero()

	bins = np.zeros(x.shape[0], dtype='int16')
	bins[bin_matrix[:,0]] = bin_matrix[:,1]

	x_bins = bins[x]
	y_bins = bins[y]

	edge_val = np.ones(x.shape[0])

	# bin_to_bin = scipy.sparse.csr_matrix(edge_val, (x_bins, y_bins), dtype='int16')
