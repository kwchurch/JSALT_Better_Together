#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>

int verbose = 0;
int show_details = 0;
int find_best = 1;
int threshold = 0;

void usage()
{
  fatal("usage: echo papers | near [--threshold|--find_best|--show_details <n>] [--map xxx] index1 index2 index3 > report");
}

struct idx {
  long *idx, nidx;
  long *idx_inv, nidx_inv;
  unsigned short *hamming_distances;
  long nhamming_distances;
};

struct node_map{
  int *old_to_new;
  int *new_to_old;
  long nold_to_new, nnew_to_old;
};

struct node_map *the_node_map = NULL;


int NEW_TO_OLD = 1;
int OLD_TO_NEW = 0;

long map_node(long node, int new_to_old)
{
  struct node_map *M = the_node_map;

  if(!M) return node;
  long N;
  int *MM;

  if(new_to_old) {
    MM = M->new_to_old;
    N = M->nnew_to_old;
  }
  else {
    MM = M->old_to_new;
    N = M->nold_to_new;
  }

  if(node < 0 || node >= N) {
    fprintf(stderr, "node = %ld; N = %ld\n", node, N);
    fatal("confusion in map_node");
  }

  return MM[node];
}
    
int good_index(struct idx *idx)
{
  return ((idx->nidx > 0) && (idx->nidx_inv == idx->nidx) && (idx->nhamming_distances+1 == idx->nidx));
}

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

void init_node_map(char *filename)
{
  char buf[1024];
  the_node_map = (struct node_map *)malloc(sizeof(struct node_map));
  if(!the_node_map) fatal("malloc failed");

  the_node_map->old_to_new = (int *)mmapfile(my_filename(buf, filename, "old_to_new.i"), &the_node_map->nold_to_new);
  the_node_map->new_to_old = (int *)mmapfile(my_filename(buf, filename, "new_to_old.i"), &the_node_map->nnew_to_old);
  the_node_map->nold_to_new /= sizeof(int);
  the_node_map->nnew_to_old /= sizeof(int);
}

void init_idx(struct idx *idx, char *filename)
{
  char buf[1024];
  memset(idx, 0, sizeof(struct idx));
  
  if(file_exists(filename)) {
    idx->idx = (long *)mmapfile(filename, &idx->nidx);
    idx->nidx /= sizeof(long);
  }

  char *fn = my_filename(buf, filename, "inv");
  if(file_exists(fn)) {
    idx->idx_inv = (long *)mmapfile(fn, &idx->nidx_inv);
    idx->nidx_inv /= sizeof(long);
  }

  fn = my_filename(buf, filename, "hamming_dist16");
  if(file_exists(fn)) {
    idx->hamming_distances = (unsigned short *)mmapfile(fn, &idx->nhamming_distances);
    idx->nhamming_distances /= sizeof(unsigned short);
  }
  if(verbose) fprintf(stderr, "init_idx: %s, %ld, %ld, %ld\n", filename, idx->nidx, idx->nidx_inv, idx->nhamming_distances);
}

struct idx *init_indexes(char **filenames, int n)
{
  int i;
  struct idx *indexes = (struct idx *)malloc(n * sizeof(struct idx));
  for(i=0; i<n; i++) {
    if(verbose) fprintf(stderr, "filenames[%d] = %s\n", i, filenames[i]);
    init_idx(indexes+i, filenames[i]);
  }
  return indexes;
}

void find_near(long *nearby_paper, int *nearby_distance, long paper, struct idx *idx)
{
  // if(verbose) fprintf(stderr, "near: %d, %ld, %ld, %ld\n", paper, idx->nidx, idx->nidx_inv, idx->nhamming_distances);

  if(paper < 0 || paper >= idx->nidx) fatal("confusion: paper is out of range");
  long offset = idx->idx_inv[paper];

  if(offset < 0 || offset >= idx->nidx) fatal("confusion: offset is out of range");
  if(offset+1 == idx->nhamming_distances) {
    fprintf(stderr, "rare case\n");
    *nearby_distance = idx->hamming_distances[offset-1];
    *nearby_paper = idx->idx[offset-1];
  }
  else {

    if(verbose) { 
      long offset_inv = idx->idx[offset];
      fprintf(stderr, "paper: %ld, offset = %ld, inv offset = %ld\n", paper, offset, offset_inv);
    }

    if(verbose && offset > 1 && offset < idx->nhamming_distances +2) {
      fprintf(stderr, "paper: %ld, nearby distances: %ld, %ld, %ld, %ld\n", paper, idx->hamming_distances[offset-1], idx->hamming_distances[offset], idx->hamming_distances[offset+1], idx->hamming_distances[offset+2]);
      fprintf(stderr, "paper: %ld, nearby papers: %ld, %ld, %ld, %ld\n", paper, idx->idx[offset-1], idx->idx[offset], idx->idx[offset+1], idx->idx[offset+2]);
    }
    *nearby_distance = idx->hamming_distances[offset];
    *nearby_paper = idx->idx[offset+1];
  }
}

void find_near_with_threshold(long old_paper_id, struct idx *idx)
{
  // if(verbose) fprintf(stderr, "near: %d, %ld, %ld, %ld\n", paper, idx->nidx, idx->nidx_inv, idx->nhamming_distances);

  long new_paper_id = map_node(old_paper_id, OLD_TO_NEW);
  if(verbose) fprintf(stderr,  "old_paper_id: %ld --> new_paper_id: %ld\n", old_paper_id, new_paper_id);

  if(new_paper_id < 0 || new_paper_id >= idx->nidx) fatal("confusion: paper is out of range");
  long offset = idx->idx_inv[new_paper_id];

  if(offset < 0 || offset >= idx->nidx) fatal("confusion: offset is out of range");
  if(offset+1 == idx->nhamming_distances) {
    fprintf(stderr, "rare case\n");
    return;
  }

  else {

    if(verbose) { 
      long offset_inv = idx->idx[offset];
      fprintf(stderr, "paper: %ld, offset = %ld, inv offset = %ld\n", new_paper_id, offset, offset_inv);
    }

    if(verbose && offset > 1 && offset < idx->nhamming_distances +2) {
      fprintf(stderr, "paper: %ld, nearby distances: %ld, %ld, %ld, %ld\n",
	      new_paper_id, idx->hamming_distances[offset-1], idx->hamming_distances[offset], idx->hamming_distances[offset+1], idx->hamming_distances[offset+2]);
      fprintf(stderr, "paper: %ld, nearby papers: %d, %d, %d, %d\n",
	      new_paper_id, idx->idx[offset-1], idx->idx[offset], idx->idx[offset+1], idx->idx[offset+2]);
    }

    long left,right;
    left=right=offset;
    int left_score,right_score;
    left_score=right_score=0;

    for(left = offset ; left >= 0; left--) {
      left_score += idx->hamming_distances[left];
      if(left_score >= threshold) break;
      printf("%ld\t%ld:%d\n", old_paper_id, map_node(idx->idx[left+1], NEW_TO_OLD), left_score);
    }

    for(right = offset ; right < idx->nidx+1; right++) {
      right_score += idx->hamming_distances[right];
      if(right_score >= threshold) break;
      if(right > offset) printf("%ld\t%ld:%d\n", old_paper_id, map_node(idx->idx[right+1], NEW_TO_OLD), right_score);
    }
  }
}

int main(int ac, char **av)
{
  int i;
  long old_paper_id;
  long nearby_paper;
  int nearby_distance;
  struct idx *indexes;
  int nindexes;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--threshold") == 0) threshold = atoi(av[++i]);
    else if(strcmp(av[i], "--find_best") == 0) find_best=atoi(av[++i]);
    else if(strcmp(av[i], "--show_details") == 0) show_details=atoi(av[++i]);
    else if(strcmp(av[i], "--map") == 0) init_node_map(av[++i]);
    else {
      if(verbose) fprintf(stderr, "i = %d; threshold = %d; find_best = %d; show_details = %d\n", i, threshold, find_best, show_details);
      nindexes=ac-i;
      indexes = init_indexes(av+i, nindexes);
      break;
    }
  }

  if(threshold > 0)
    while(scanf("%ld", &old_paper_id) == 1) {
      for(i=0;i<nindexes;i++)
	if(good_index(indexes+i))
	  find_near_with_threshold(old_paper_id, indexes + i);
  }
      
  else
    while(scanf("%ld", &old_paper_id) == 1) {
      int best_distance = 65535;
      int best_index = -1;
      long best_paper = 1;
    
      long new_paper_id = map_node(old_paper_id, OLD_TO_NEW);

      printf("%ld", old_paper_id);
      for(i=0;i<nindexes;i++) {
	if(good_index(indexes+i)) {
	  find_near(&nearby_paper, &nearby_distance, new_paper_id, indexes + i);
	  if(new_paper_id != nearby_paper && nearby_distance < best_distance) {
	    best_index=i;
	    best_distance = nearby_distance;
	    best_paper = nearby_paper;
	  }
	  if(show_details > 0) printf("\t%ld:%d", map_node(nearby_paper, NEW_TO_OLD), nearby_distance);
	  if(show_details > 0 && find_best > 0) printf(":%ld:%d:%d", map_node(best_paper, NEW_TO_OLD), best_distance, best_index);
	}
	else if(show_details > 0) printf("\tNA");
      }
    
      if(find_best > 0)
	printf("\t%ld:%d:%d\n", map_node(best_paper, NEW_TO_OLD), best_distance, best_index);
      else putchar('\n'); 
    }
}
