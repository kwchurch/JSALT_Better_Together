#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "util.h"

void usage()
{
  fprintf(stderr, "usage: invert_landmarks --docs start,end --number_of_landmarks 100 --input_landmarks landmarks.i --output_postings postings  --tick 100\n");
  fatal("usage");
}

struct pair {
  int landmark;
  int id;
};

int pair_compare(struct pair *a, struct pair *b)
{
  if(a->landmark < b->landmark) return -1;
  if(a->landmark > b->landmark) return 1;
  if(a->id < b->id) return -1;
  if(a->id > b->id) return 1;
  return 0;
}
  


int my_max(int *vec, long n)
{
  int result = *vec;
  int *end = vec + n;
  for(; vec<end;vec++)
    if(*vec > result) result=*vec;
  return result;
}

int my_min(int *vec, long n)
{
  int result = *vec;
  int *end = vec + n;
  for(; vec<end;vec++)
    if(*vec < result) result=*vec;
  return result;
}


int *hist(int *vec, long N, long *nhist)
{
  int minv = my_min(vec, N);
  int maxv = my_max(vec, N);
  
  if(minv < 0) fatal("hist: expected array to have no values less than 0");

  int n = 1+my_max(vec, N);
  *nhist = n;
  
  int *result = (int *)malloc(sizeof(int) * n);
  if(!result) fatal("malloc failed");
  memset(result, 0, sizeof(int)*n);
  int *end = vec+N;
  for(;vec<end;vec++)
    result[*vec]++;
  return result;
}

long *cumhist(int *hist, long N)
{
  long i;
  long *result = (long *)malloc(sizeof(long) * N);
  if(!result) fatal("cumhist: malloc failed");

  *result = hist[0];
  for(i=1;i<N;i++)
    result[i] = result[i-1] + hist[i];
  return result;
}

void output_longs(long *longs, long n, char *fn)
{
  fprintf(stderr, "output_longs: n = %ld, fn = %s\n", n, fn);

  FILE *fd = fopen(fn, "wb");
  if(!fd) fatal("open failed");
  if(fwrite(longs, sizeof(long), n, fd) != n)
    fatal("write failed");
  fclose(fd);
}


void output_pairs(struct pair *pairs, long n, char *fn)
{
  fprintf(stderr, "output_pairs: n = %ld, fn = %s\n", n, fn);

  FILE *fd = fopen(fn, "wb");
  if(!fd) fatal("open failed");
  if(fwrite(pairs, sizeof(*pairs), n, fd) != n)
    fatal("write failed");
  fclose(fd);
}


void output_ints(int *ints, long n, char *fn)
{
  fprintf(stderr, "output_ints: n = %ld, fn = %s\n", n, fn);

  FILE *fd = fopen(fn, "wb");
  if(!fd) fatal("open failed");
  if(fwrite(ints, sizeof(int), n, fd) != n)
    fatal("write failed");
  fclose(fd);
}

int main(int ac, char **av)
{
  int tick = -1;
  int i, j;
  char filename_buf[256];
  int number_of_landmarks = 0;
  int *landmarks = NULL;
  char *postings = NULL;
  long nlandmarks;
  int docs_start = 0;
  int docs_end = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--number_of_landmarks") == 0) number_of_landmarks = atoi(av[++i]);
    else if(strcmp(av[i], "--input_landmarks") == 0) {
      landmarks = (int *)mmapfile(av[++i], &nlandmarks);
      nlandmarks /= sizeof(int);
    }
    else if(strcmp(av[i], "--output_postings") == 0) postings = av[++i];
    else if(strcmp(av[i], "--tick") == 0) tick = atoi(av[++i]);
    else if(strcmp(av[i], "--docs") == 0) sscanf(av[++i], "%d,%d", &docs_start, &docs_end);
    else {
      fprintf(stderr, "i=%d, av[i] = %s\n", i, av[i]);
      usage();
    }
  }

  if(!postings) {
    fprintf(stderr, "--postings arg is required\n");
    usage();
  }

  if(!landmarks) {
    fprintf(stderr, "--landmarks arg is required\n");
    usage();
  }

  if(!number_of_landmarks) {
    fprintf(stderr, "--number_ob_landmarks arg is required\n");
    usage();
  }

  long Ndocs = nlandmarks/number_of_landmarks;
  long doc;
  if(docs_end < 0 || docs_end > Ndocs)
    docs_end = Ndocs;

  long npairs = (docs_end - docs_start) * number_of_landmarks;
  struct pair *pairs = (struct pair *)malloc(sizeof(struct pair) * npairs);
  if(!pairs) fatal("malloc failed");

  struct pair *p=pairs;

  for(doc=docs_start; doc< docs_end; doc++) 
    for(j=0;j<number_of_landmarks;j++) {
      long offset = doc*number_of_landmarks+j;
      if(offset >= nlandmarks) {
	fprintf(stderr, "offset is too large: offset = %ld, doc = %ld, j = %d, nlandmarks = %ld\n", offset, doc, j, nlandmarks);
	fatal("assertion failed");
      }
      
      p->id = doc;
      p->landmark = landmarks[offset];

      if(tick > 0 && (p->id % tick == 0))
	fprintf(stderr, "doc: %d\tlandmark: %d\n", p->id, p->landmark);
      p++;
  }

  fprintf(stderr, "about to sort\n");
  fflush(stderr);
  qsort(pairs, p-pairs, sizeof(*p), pair_compare);

  fprintf(stderr, "about to output results\n");
  fflush(stderr);
  output_pairs(pairs, p-pairs, filename(filename_buf, postings, "pairs"));
  fprintf(stderr, "done\n");
  exit(0);
}
