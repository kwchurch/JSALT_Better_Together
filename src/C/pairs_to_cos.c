#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <stdlib.h>
#include <stdlib.h>
#include <search.h>

int verbose = 0;

void usage()
{
  fatal("usage: pairs_to_cos --input_new_pairs --verbose --dir \n or\n pairs_to_cos --floats floats --record_size K [--map xxx] [--new_map xxx.L] < pairs");
}

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
    long *found = bsearch(&node, new_map, nnew_map, sizeof(long), long_compare);
    // long *found = bsearch(&node, new_map, nnew_map, sizeof(long), (__compar_fn_t)long_compare);
    if(!found) return -1;
    if(found < new_map || found >= new_map + nnew_map) fatal("confusion in new_map_node");
    return found - new_map;
  }
}

long map_node(long node, int new_to_old, int no_map)
{

  if(no_map) return node;

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
    return -1;
    // fatal("confusion in map_node");
  }

  return MM[node];
}


float *floats = NULL;
long nfloats = -1;
int record_size = -1;
long max_new = -1;

double dot(float *a, float *b, int n)
{
  double res = 0;
  float *end = a+n;
  while(a<end)
    res += *a++ * *b++;
  return res;
}

double SMALL = 1e-10;

double norm(float *a, int n)
{
  double res = 0;
  float *end = a+n;
  while(a<end) {
    float aa = *a++;
    res += aa * aa;
  }
  return sqrt(res);
}

double my_cos(float alen, float *a, float *b, int n)
{
  // double alen = norm(a, n);
  if(alen < SMALL) return -1.0;
  double blen = norm(b, n);
  if(blen < SMALL) return -1.0;
  return dot(a, b, n)/(alen * blen);
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

void get_args_from_dir(char *dir)
{
  if(verbose) fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  if(!fd) {
    fprintf(stderr, "pairs_to_cos: %s/record_size\n", dir);
    fatal("open failed");
  }

  fscanf(fd, "%d", &record_size);
  fclose(fd);
  
  sprintf(buf, "%s/embedding.f", dir);
  floats = (float *)mmapfile(buf, &nfloats);
  nfloats /= sizeof(float);
  max_new = nfloats/record_size;
  // fprintf(stderr, "record_size = %d, max_new = %ld, sizeof(float) = %d\n", record_size, max_new, sizeof(float));
  
  sprintf(buf, "%s/map", dir);
  init_node_map(buf);
  // fprintf(stderr, "leaving, get_args_from_dir: %s\n", dir);
}    

int main(int ac, char **av)
{
  int input_new_pairs = 0;
  int no_map = 1;
  long prev_i=-1, i;
  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--verbose") == 0) verbose++;
    else if(strcmp(av[i], "--input_new_pairs") == 0) input_new_pairs=1;
    else if(strcmp(av[i], "--dir") == 0) {
      no_map = 0;
      get_args_from_dir(av[++i]);
    }
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--floats") == 0) {
      floats = (float *)mmapfile(av[++i], &nfloats);
      nfloats /= sizeof(float);
    }
    else if(strcmp(av[i], "--map") == 0) {
      no_map = 0;
      init_node_map(av[++i]);
    }
    else if(strcmp(av[i], "--new_map") == 0) {
      no_map = 0;
      new_map = (long *)mmapfile(av[++i], &nnew_map);
      nnew_map /= sizeof(long);
    }
    else usage();
  }

  if(record_size <= 0) fatal("bad record_size");
  if(nfloats <= 0) fatal("bad input: --floats");

  double d, alen = 0;
  if (input_new_pairs > 0) {
    long new_i, new_j;
    while(scanf("%ld%ld", &new_i, &new_j) == 2) {
      long old_i = map_node(new_i, NEW_TO_OLD, no_map);
      long old_j = map_node(new_j, NEW_TO_OLD, no_map);
      if(prev_i != new_i) {
	alen = norm(floats + new_i * record_size, record_size);
	prev_i = new_i;
      }
      d = my_cos(alen, floats + new_i * record_size, floats + new_j * record_size, record_size);
      printf("%f\t%ld\t%ld\n", d, old_i, old_j);
    }
  }
  else {
    long old_i, old_j;
    while(scanf("%ld%ld", &old_i, &old_j) == 2) {
      long new_i = map_node(old_i, OLD_TO_NEW, no_map);
      long new_j = map_node(old_j, OLD_TO_NEW, no_map);
      // really should not confuse doc 0 with NA, but that may be hard to fix for now
      if(new_i <= 0 || new_j <= 0 || new_i >=  max_new || new_j >= max_new) {
	printf("-1\t%ld\t%ld\n", old_i, old_j);
	continue;
      }
      if(prev_i != new_i) {
	alen = norm(floats + new_i * record_size, record_size);
	prev_i = new_i;
      }
      d = my_cos(alen, floats + new_i * record_size, floats + new_j * record_size, record_size);
      printf("%f\t%ld\t%ld\n", d, old_i, old_j);
    }
  }
  
  exit(0);

}
