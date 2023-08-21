#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>
#include <search.h>

int verbose = 0;
// int show_details = 0;
// int find_best = 1;
// int threshold = 0;
int record_size = -1;
int no_map = 1;
struct idx *indexes;
int nindexes = -1;
int offset = -1;
int n_candidates = 100;
int skip_cos = 0;

void usage()
{
  fatal("usage: echo papers | faster_near_with_floats --dir <dir> [--offset <n>] [--n_candidates <n>] [--skip_cos] index1 index2 index3 > report");
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

struct long_node_map{
  long *old_to_new;
  long *new_to_old;
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
  if(a == floats || b == floats) return -1.0;

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
  if(paper < 0 || paper >= idx->nidx) {
    fprintf(stderr, "paper = %ld\n", paper);
    fatal("confusion: paper is out of range");
  }
  long o = idx->idx_inv[paper];

  if(o < 0 || o >= idx->nidx) fatal("confusion: o is out of range");

  long start = o - offset;
  long end = o + offset;
  if(start < 0) start=0;
  if(end >= idx->nidx) end = idx->nidx - 1;
  *nfound = end - start;
  return idx->idx + start;
}

void get_args_from_dir(char *dir)
{
  // fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  fscanf(fd, "%d", &record_size);
  // fprintf(stderr, "record_size: %d\n", record_size);
  fclose(fd);
  
  if(!skip_cos) {
    sprintf(buf, "%s/embedding.f", dir);
    floats = (float *)mmapfile(buf, &nfloats);
    nfloats /= sizeof(float);
  }

  sprintf(buf, "%s/map", dir);
  init_node_map(buf);
  // fprintf(stderr, "leaving, get_args_from_dir: %s\n", dir);
}    

void output_score(long old_i, long new_i, long old_j, long new_j, int freq)
{
  if(skip_cos) printf("%d\t%ld\t%ld\n",  freq, old_i, old_j);
  else {
    float score = my_cos(floats + new_j * record_size, floats + new_i * record_size, record_size);
    printf("%f\t%ld\t%ld\n", score, old_i, old_j);
  }
}

#define MAXCOUNTS 100

void do_it(long old_paper_id, long *buf)
{
  int i, j;
  long *buf_ptr = buf;
  long new_paper_id = map_node(old_paper_id, OLD_TO_NEW, no_map);
  if(!skip_cos) {
    double paper_norm = norm(floats + new_paper_id * record_size, record_size);
    fprintf(stderr, "corpus_id: %ld; norm = %f\n", old_paper_id, paper_norm);
    if(paper_norm < SMALL) {
      fprintf(stderr, "warning, norm for corpusid %ld is too small\n", old_paper_id);
      return;
    }
  }
  if(verbose) fprintf(stderr, "old_paper_id = %ld, new_paper_id = %ld\n", old_paper_id, new_paper_id);
  for(i=0;i<nindexes;i++) {
    if(verbose) fprintf(stderr, "i=%d, good = %d\n", i, good_index(indexes+i));
    if(good_index(indexes+i) && new_paper_id >= 0) {
      int nfound;
      long *found = find_near(new_paper_id, indexes + i, offset, &nfound);
      memcpy(buf_ptr, found, sizeof(long) * nfound);
      buf_ptr += nfound;
    }
  }
  long nbuf = buf_ptr - buf;
  qsort(buf, nbuf, sizeof(long), long_compare);

  int counts[MAXCOUNTS];
  memset(counts, 0, sizeof(counts));

  for(i=0; i<nbuf; i=j) {
    for(j=i+1;j<nbuf && buf[i] == buf[j]; j++) ;
    int freq = j - i;
    if(freq > MAXCOUNTS-1) freq=MAXCOUNTS;
    counts[freq]++;
  }

  int candidates=0;
  int freq_threshold = MAXCOUNTS-1;
  while(freq_threshold >= 0 && candidates < n_candidates) {
    candidates += counts[freq_threshold];
    freq_threshold--;
  }

  fprintf(stderr, "corpusid: %ld, freq_threshold = %d, outputing %d candidates\n", old_paper_id, freq_threshold, candidates);

  for(i=0; i<nbuf; i=j) {
    for(j=i+1;j<nbuf && buf[i] == buf[j]; j++) ;
    int freq = j - i;
    if(freq > freq_threshold) {
      long new_j = buf[i];
      long old_j = map_node(new_j, NEW_TO_OLD, no_map);
      output_score(old_paper_id, new_paper_id, old_j, new_j, freq);
    }
  }
}

int main(int ac, char **av)
{
  int i;
  long old_paper_id;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--dir") == 0) {
      no_map = 0;
      get_args_from_dir(av[++i]);
    }
    else if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--verbose") == 0) verbose++;
    // else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--offset") == 0) offset = atoi(av[++i]);
    else if(strcmp(av[i], "--n_candidates") == 0) n_candidates = atoi(av[++i]);
    else if(strcmp(av[i], "--skip_cos") == 0) skip_cos=1;

    /* else if(strcmp(av[i], "--floats") == 0) { */
    /*   floats = (float *)mmapfile(av[++i], &nfloats); */
    /*   nfloats /= sizeof(float); */
    /* } */
    /* else if(strcmp(av[i], "--map") == 0) { */
    /*   no_map = 0; */
    /*   init_node_map(av[++i]); */
    /* } */
    /* else if(strcmp(av[i], "--new_map") == 0) { */
    /*   no_map = 0; */
    /*   new_map = (long *)mmapfile(av[++i], &nnew_map); */
    /*   nnew_map /= sizeof(long); */
    /* } */
    /* else if(strcmp(av[i], "--urls") == 0) init_urls(av[++i]); */
    else {
      nindexes=ac-i;
      indexes = init_indexes(av+i, nindexes);
      break;
    }
  }

  if(!skip_cos && ! floats) fatal("no floats???");
  if(nindexes <= 0) fatal("no indexes???");
  if(offset <= 0) fatal("--offset arg is required");
  if(record_size <= 0) fatal("--record_size arg is required");

  long *buf = (long *)malloc(sizeof(long) * offset * 2 * nindexes);

  while(scanf("%ld", &old_paper_id) == 1)
    do_it(old_paper_id, buf);

  return 0;
}
