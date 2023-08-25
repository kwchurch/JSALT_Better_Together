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
int record_size = -1;

void usage()
{
  fatal("usage: echo old_paper_id | brute_force_with_floats [--dir embedding directory] [--record_size <n>] [--floats <file>] [--threshold 0] > report");
}
    
char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

int long_compare(long *a, long *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

float *floats;
long nfloats;
long N;

struct node_map{
  int *old_to_new;
  int *new_to_old;
  long nold_to_new, nnew_to_old;
};

struct long_node_map{
  long *old_to_new;
  long *new_to_old;
  long nold_to_new, nnew_to_old;
};

long *new_map = NULL;
long nnew_map = 0;

struct node_map *the_node_map = NULL;
struct long_node_map *the_long_node_map = NULL;

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
    if(found < new_map || found >= new_map + nnew_map) return -1; /* fatal("confusion in new_map_node"); */
    return found - new_map;
  }
}

long map_node(long node, int new_to_old, int no_map)
{

  if(no_map) return node;

  if(new_map) return new_map_node(node, new_to_old);

  if(the_node_map) {
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

  if(the_long_node_map) {
    struct long_node_map *M = the_long_node_map;

    // fprintf(stderr, "map_node: node = %ld, new_to_old  = %d\n", node, new_to_old);

    if(!M) return node;
    long N;
    long *MM;

    if(new_to_old) {
      MM = M->new_to_old;
      N = M->nnew_to_old;
      return MM[node];
    }
    else {
      MM = M->old_to_new;
      N = M->nold_to_new;

      // fprintf(stderr, "map_node: node = %ld, binary search\n", node, new_to_old);

      long *found = bsearch(&node, MM, N, sizeof(long), long_compare);
      // long *found = bsearch(&node, new_map, nnew_map, sizeof(long), (__compar_fn_t)long_compare);

      if(!found) {
	// fprintf(stderr, "not found\n");
	return -1;
      }
      if(found < MM || found >= MM + N) {
	// fprintf(stderr, "found is out of range\n");
	return -1; /* fatal("confusion in new_map_node"); */
      }

      // fprintf(stderr, "map_node: node = %ld, found = %ld\n", node, found-MM);
      return found - MM;
    }

    if(node < 0 || node >= N) {
      fprintf(stderr, "warning, node = %ld; N = %ld\n", node, N);
      return -1;
      // fatal("confusion in map_node");
    }

    // return MM[node];
  }
  
  else fatal("confusion in map_node");
}
    
float *floats = NULL;
long nfloats = -1;
// long N;


void init_node_map(char *filename)
{
  char buf[1024];
  if(file_exists(my_filename(buf, filename, "old_to_new.i"))) {

    // fprintf(stderr, "init_node_map: old case\n"); 
    the_node_map = (struct node_map *)malloc(sizeof(struct node_map));
    if(!the_node_map) fatal("malloc failed");


    the_node_map->old_to_new = (int *)mmapfile(my_filename(buf, filename, "old_to_new.i"), &the_node_map->nold_to_new);
    the_node_map->new_to_old = (int *)mmapfile(my_filename(buf, filename, "new_to_old.i"), &the_node_map->nnew_to_old);
    the_node_map->nold_to_new /= sizeof(int);
    the_node_map->nnew_to_old /= sizeof(int);
  }
  else {

    // fprintf(stderr, "init_node_map: new case\n"); 
    the_long_node_map = (struct long_node_map *)malloc(sizeof(struct long_node_map));
    if(!the_long_node_map) fatal("malloc failed");

    the_long_node_map->old_to_new = (long *)mmapfile(my_filename(buf, filename, "old_to_new.sorted.L"), &the_long_node_map->nold_to_new);
    the_long_node_map->new_to_old = (long *)mmapfile(my_filename(buf, filename, "new_to_old.L"), &the_long_node_map->nnew_to_old);
    the_long_node_map->nold_to_new /= sizeof(long);
    the_long_node_map->nnew_to_old /= sizeof(long);
  }
}


void get_args_from_dir(char *dir)
{
  fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  fscanf(fd, "%d", &record_size);
  fprintf(stderr, "record_size: %d\n", record_size);
  fclose(fd);
  
  sprintf(buf, "%s/embedding.f", dir);
  floats = (float *)mmapfile(buf, &nfloats);
  nfloats /= sizeof(float);

  sprintf(buf, "%s/map", dir);
  init_node_map(buf);
  fprintf(stderr, "leaving, get_args_from_dir: %s\n", dir);
}    




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

double my_cos(float *a, float *b, int n, double alen)
{
  // double alen = norm(a, n);
  // if(alen < SMALL) return -2.0;
  double blen = norm(b, n);
  if(blen < SMALL) return -2.0;
  double res = dot(a, b, n)/(alen * blen);
  // fprintf(stderr, "res = %f, alen = %f, blen = %f, n = %d\n", res, alen, blen, n);
  return res;
}


int main(int ac, char **av)
{
  int i;
  float threshold = -2.0;
  // FILE *fd = NULL;
  int no_map = 1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--dir") == 0) {
      no_map = 0;
      get_args_from_dir(av[++i]);
    }
    else if(strcmp(av[i], "--threshold") == 0) threshold = atof(av[++i]);
    else if(strcmp(av[i], "--help") == 0) usage();
    // else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    /* else if(strcmp(av[i], "--floats") == 0) { */
    /*   char *fn = av[++i]; */
    /*   floats = (float *)mmapfile(fn, &nfloats); */
    /*   nfloats /= sizeof(float); */
    /*   fd = fopen(fn, "rb"); */
    /*   if(!fd) fatal("open failed"); */
    /* } */
    else usage();
  }

  if(record_size <= 0) fatal("--record_size arg is required");

  // long new_paper_id = 7375270;
  long j, old_paper_id;
  while(scanf("%ld", &old_paper_id) == 1) {
    long new_paper_id = map_node(old_paper_id, OLD_TO_NEW, no_map);
    // fseek(fd, 0, SEEK_SET);
    // float *f = (float *)malloc(sizeof(float) * record_size);
    if(new_paper_id <= 0) continue;
    float *query = floats + new_paper_id * record_size;
    double qlen = norm(query, record_size);     
    if(qlen < SMALL) continue;
    for(j=0; j*record_size < nfloats;j++) {
      // if(j > 10650966) fprintf(stderr,"j=%ld\n", j);
      // if(fread(f, sizeof(float), record_size, fd) != record_size) break;
      float *f = floats + j * record_size;
      double score = my_cos(f, query, record_size, qlen);
      if(score > threshold)	 
	printf("%f\t%ld\t%ld\n", score, old_paper_id, map_node(j, NEW_TO_OLD, no_map));
    }
  }
}
