#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <errno.h>
#include <strings.h>

int verbose = 0;
int show_details = 0;
int find_best = 1;
int threshold = 0;

void usage()
{
  fatal("usage: echo papers | select_vectors [--record_size <n>] [--floats <file>] [--map xxx] [--new_map xxx.L] > vectors");
}

struct idx {
  long *idx, nidx;
  long *idx_inv, nidx_inv;
};

struct node_map{
  int *old_to_new;
  int *new_to_old;
  long nold_to_new, nnew_to_old;
};

int long_compare(long *a, long *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

long *new_map = NULL;
long nnew_map = 0;

struct node_map *the_node_map = NULL;

int NEW_TO_OLD = 1;
int OLD_TO_NEW = 0;

long new_map_node(long node, int new_to_old)
{
  if(new_to_old == NEW_TO_OLD) {
    if(node < 0 || node >= nnew_map) {
      fprintf(stderr, "warning: new_map_node, %ld is out of range\n", node);
      return -1;
    }
    return new_map[node];
  }
  else { 
    long *found = bsearch(&node, new_map, nnew_map, sizeof(long), (__compar_fn_t)long_compare);
    if(!found) return -1;
    if(found < new_map || found >= new_map + nnew_map) fatal("confusion in new_map_node");
    return found - new_map;
  }
}

long map_node(long node, int new_to_old)
{

  if(new_map) return new_map_node(node, new_to_old);

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
    fprintf(stderr, "warning, node = %ld; N = %ld\n", node, N);
    // return -1;
    fatal("confusion in map_node");
  }

  return MM[node];
}
    
float *floats = NULL;
long nfloats = -1;

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

void output_zeros(int n)
{
  float zero = 0;
  int i;
  for(i=0;i<n;i++)
    if(fwrite(&zero, sizeof(float), 1, stdout) != 1)
      fatal("write failed");
}

int main(int ac, char **av)
{
  int i;
  long old_paper_id;
  int record_size = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--floats") == 0) {
      floats = (float *)mmapfile(av[++i], &nfloats);
      nfloats /= sizeof(float);
    }
    else if(strcmp(av[i], "--map") == 0) init_node_map(av[++i]);
    else if(strcmp(av[i], "--new_map") == 0) {
      new_map = (long *)mmapfile(av[++i], &nnew_map);
      nnew_map /= sizeof(long);
    }
    else usage();
  }

  if(! floats) fatal("no floats???");
  if(record_size <= 0) fatal("--record_size arg is required");

  while(scanf("%ld", &old_paper_id) == 1) {
    if(old_paper_id < 0) output_zeros(record_size);
    else {
      long new_paper_id = map_node(old_paper_id, OLD_TO_NEW);
      fprintf(stderr, "old_paper_id = %ld, new_paper_id = %ld\n", old_paper_id, new_paper_id);
      if(fwrite(floats + new_paper_id * record_size, sizeof(float), record_size, stdout) != record_size)
	fatal("write failed");
    }
  }
}


