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
  fatal("usage: score_with_floats [--record_size <n>] [--floats <file>] index1 index2 index3 < keys > report");
}

struct idx {
  char *fn;
  long *idx, nidx;
  long *idx_inv, nidx_inv;
};

int long_compare(long *a, long *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
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

void init_idx(struct idx *idx, char *filename)
{
  char buf[1024];
  memset(idx, 0, sizeof(struct idx));
  
  if(file_exists(filename)) {
    idx->fn = filename;
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

int main(int ac, char **av)
{
  int i;
  int summarize = 0;
  struct idx *indexes;
  int nindexes = -1;
  int record_size = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--summarize") == 0) summarize++;
    else if(strcmp(av[i], "--floats") == 0) {
      floats = (float *)mmapfile(av[++i], &nfloats);
      nfloats /= sizeof(float);
    }
    else {
      nindexes=ac-i;
      indexes = init_indexes(av+i, nindexes);
      break;
    }
  }

  if(nindexes <= 0) fatal("no indexes???");
  if(record_size <= 0) fatal("--record_size arg is required");

  long key, line=0;
  
  if (summarize > 0) {
    double *sums = (double *)malloc(sizeof(double) * nindexes);
    memset(sums, 0, sizeof(double) * nindexes);
      
    while(scanf("%ld", &key) == 1) {
      line++;
      for(i=0;i<nindexes;i++) {
	if(good_index(indexes+i)) {
	  long *j = &indexes[i].idx[key];
	  sums[i] += my_cos(floats + j[0] * record_size, floats + j[1] * record_size, record_size);
	}
      }
    }
    for(i=0;i<nindexes;i++)
      printf("%f\t%s\n", sums[i]/line, indexes[i].fn);
  }

  else 
    while(scanf("%ld", &key) == 1) {
      for(i=0;i<nindexes;i++) {
	if(good_index(indexes+i)) {
	  long *j = &indexes[i].idx[key];
	  printf("%f\t", my_cos(floats + j[0] * record_size, floats + j[1] * record_size, record_size));
	}
      }
      printf("%ld\n", key);
    }
}


