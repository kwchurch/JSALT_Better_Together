#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <search.h>

int verbose = 0;
int show_details = 0;
int find_best = 1;
int threshold = 0;

void usage()
{
  fatal("usage: echo <pairs of papers> | near_with_floats [--input_new_pairs] [--record_size <n>] [--floats <file>] [--map xxx] [--new_map xxx.L] [--urls xxx] > report");
}

struct urls {
  char *lines;
  unsigned int *idx;
  long nidx;
  long nlines;
} *urls = NULL;

void init_urls(char *fn) {
  char buf[1024];
  urls = (struct urls *)malloc(sizeof(struct urls));
  urls->lines = (char *)mmapfile(fn, &urls->nlines);
  sprintf(buf, "%s.line_index.i", fn);
  urls->idx = (unsigned int *)mmapfile(buf, &urls->nidx);
  urls->nidx /= sizeof(int);
}

char *id2url(char *buf, long old_id, long new_id)
{
  if(!urls) sprintf(buf, "%ld", old_id);
  else if(new_id >= urls->nidx) sprintf(buf, "<a href=\"https://www.semanticscholar.org/author/%ld\">%ld</a>", old_id, old_id);
  else {
    // fprintf(stderr, "id2url[%ld]=%d\n", id, urls->idx[id]);
    char *res = urls->lines + urls->idx[new_id];
    int i;
    for(i=0;i<1023;i++) {
      buf[i]=res[i];
      if(res[i] == '\n') break;
    }
    buf[i]=0;
  }
  return buf;    
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
    long *found = bsearch(&node, new_map, nnew_map, sizeof(long), long_compare);
    // long *found = bsearch(&node, new_map, nnew_map, sizeof(long), (__compar_fn_t)long_compare);
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
    
float *floats;
long nfloats;
long N;

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

double my_cos(float *a, float *b, int n)
{
  double alen = norm(a, n);
  if(alen < SMALL) return -1.0;
  double blen = norm(b, n);
  if(blen < SMALL) return -1.0;
  double res = dot(a, b, n)/(alen * blen);
  // fprintf(stderr, "res = %f, alen = %f, blen = %f, n = %d\n", res, alen, blen, n);
  return res;
}

int good_index(struct idx *idx)
{
  return ((idx->nidx > 0) && (idx->nidx_inv == idx->nidx));
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

  if(verbose) fprintf(stderr, "init_idx: %s, %ld, %ld\n", filename, idx->nidx, idx->nidx_inv);
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

long *find_near(long paper, struct idx *idx, int offset, int *nfound)
{
  if(paper < 0 || paper >= idx->nidx) fatal("confusion: paper is out of range");
  long o = idx->idx_inv[paper];

  if(o < 0 || o >= idx->nidx) fatal("confusion: o is out of range");

  long start = o - offset;
  long end = o + offset;
  if(start < 0) start=0;
  if(end >= idx->nidx) end = idx->nidx - 1;
  *nfound = end - start;
  return idx->idx + start;
}

int main(int ac, char **av)
{
  fatal("deprecated: use pairs_to_cos");

  char buf[2][1024];
  int i;
  int input_new_pairs = 0;
  long old_paper_id[2];
  long new_paper_id[2];
  // struct idx *indexes;
  // int nindexes = -1;
  int record_size = -1;
  // int offset = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--input_new_pairs") == 0) input_new_pairs++;
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    // else if(strcmp(av[i], "--offset") == 0) offset = atoi(av[++i]);
    else if(strcmp(av[i], "--floats") == 0) {
      floats = (float *)mmapfile(av[++i], &nfloats);
      nfloats /= sizeof(float);
    }
    else if(strcmp(av[i], "--map") == 0) init_node_map(av[++i]);
    else if(strcmp(av[i], "--new_map") == 0) {
      new_map = (long *)mmapfile(av[++i], &nnew_map);
      nnew_map /= sizeof(long);
    }
    else if(strcmp(av[i], "--urls") == 0) init_urls(av[++i]);
    else usage();
  }

  // if(nindexes <= 0) fatal("no indexes???");
  // if(offset <= 0) fatal("--offset arg is required");

  if(record_size <= 0) fatal("--record_size arg is required");

  while(fgets(buf[0], 1024, stdin) != NULL) {
    if(sscanf(buf[0], "%ld%ld", &old_paper_id[0], &old_paper_id[1]) != 2) 
      printf("-1\t%s", buf[0]);
    else {

      new_paper_id[0] = map_node(old_paper_id[0], OLD_TO_NEW);
      new_paper_id[1] = map_node(old_paper_id[1], OLD_TO_NEW);

      printf("%f\t%s\t%s\t%ld\t%ld\t%ld\t%ld\n",
	     my_cos(floats + new_paper_id[0] * record_size, floats + new_paper_id[1] * record_size, record_size),
	     id2url(buf[0], old_paper_id[0], new_paper_id[0]),
	     id2url(buf[1], old_paper_id[1], new_paper_id[1]),
	     old_paper_id[0], old_paper_id[1], 
	     new_paper_id[0], new_paper_id[1]);
    }
  }
}
