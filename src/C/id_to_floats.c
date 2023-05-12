#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <stdlib.h>
#include <search.h>

void usage()
{
  fatal("usage: id_to_floats --dir \n or\n id_to_floats --floats floats --record_size K [--map xxx] [--new_map xxx.L] < pairs");
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
    return -1;
    // fatal("confusion in map_node");
  }

  return MM[node];
}


float *floats = NULL;
long nfloats = -1;
int record_size = -1;

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
void return_floats(float *fltlist, int how_many)
{
    int i;
    for(i = 0; i < how_many; i++)
    {
        printf(" %f", fltlist[i]);
    }
}

void get_args_from_dir(char *dir)
{
  // fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  fscanf(fd, "%d", &record_size);
  fclose(fd);

  // fprintf(stderr, "record_size = %d\n", record_size);
  
  sprintf(buf, "%s/embedding.f", dir);
  floats = (float *)mmapfile(buf, &nfloats);
  nfloats /= sizeof(float);

  sprintf(buf, "%s/map", dir);
  init_node_map(buf);
  // fprintf(stderr, "leaving, get_args_from_dir: %s\n", dir);
}    

int main(int ac, char **av)
{

  float *zeros = NULL;
  int binary_output = 0;
  long prev_i=-1, i, j;
  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--dir") == 0) get_args_from_dir(av[++i]);
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
    else if(strcmp(av[i], "--binary_output") == 0) binary_output=1;
    else usage();
  }

  if(record_size <= 0) fatal("bad record_size");
  if(nfloats <= 0) fatal("bad input: --floats");

  //double d, alen = 0;
  while(scanf("%ld", &i) == 1) {
    long new_i = map_node(i, OLD_TO_NEW);

    if(binary_output) {
      if(new_i < 0) {
	if(!zeros) {
	  zeros = (float *)malloc(sizeof(float) * record_size);
	  if(!zeros) fatal("malloc failed");
	  memset(zeros, 0, sizeof(float) * record_size);
	}
	if(fwrite(zeros, sizeof(float), record_size, stdout) != record_size)
	  fatal("write failed");
      }
      else if(fwrite(floats + new_i * record_size, sizeof(float), record_size, stdout) != record_size)
	fatal("write failed");
    }
    else {
      printf("%ld %ld", i, new_i);
      return_floats(floats + new_i * record_size, record_size);
      printf("\n");
    }
  }
  
  exit(0);

}
