#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <memory.h>
#include <stdlib.h>

int verbose = 0;

int *malloc_ints(long n)
{
  // fprintf(stderr, "malloc_ints: n = %ld\n", n);
  int *res = (int *)malloc(n * sizeof(int));
  if(!res) fatal("malloc_ints: failed");
  // should not be necessary
  memset(res, 0, n * sizeof(int));
  // fprintf(stderr, "malloc_ints: done\n", n);
  return res;
}

long *malloc_longs(long n)
{
  // fprintf(stderr, "malloc_longs: n = %ld\n", n);
  long *res = (long *)malloc(n * sizeof(long));
  if(!res) fatal("malloc_ints: failed");
  // should not be necessary
  memset(res, 0, n * sizeof(long));
  // fprintf(stderr, "malloc_longs: done\n", n);
  return res;
}



int intcomp(int *a,  int *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

// return 1 on success
int check_order(int *X, long N)
{
  long i;
  for(i=1;i<N;i++)
    if(intcomp(&X[i-1], &X[i]) > 0)
      return 0;
  return 1;
}

long *cumsum(long *X, long N)
{
  // fprintf(stderr, "calling cumsum: N = %ld\n", N);

  long i;
  long *res = malloc_longs(N+1);
  if(!res) fatal("malloc failed");
  res[0] = 0;
  for(i = 0; i<N; i++)
    res[i+1] = res[i] + X[i];
  return res;
}

long *index_ints(int *X, long N, long *nresult)
{
  fprintf(stderr, "calling index_ints\n");
  long i, n = X[N-1]+1;
  *nresult = n+1;
  long *res = (long *)malloc(sizeof(long) * n);
  if(!res) fatal("malloc failed");
  memset(res, 0, sizeof(long)*n);
  for(i=0;i<N;i++)
    res[X[i]]++;
  return cumsum(res, N);
}

long *memoize_index(char *filename, int *X, long N)
{
  // fprintf(stderr, "calling memoize_index: %s\n", filename);
  char buf[1024];
  sprintf(buf, "%s.idx", filename);
  FILE *fd = fopen(buf, "rb");
  long nres;
  if(!fd) {
    FILE *fd = fopen(buf, "wb");
    long *res = index_ints(X, N, &nres);
    // fprintf(stderr, "index_size = %ld\n", nres);
    if(fwrite(res, sizeof(long), nres, fd) != nres)
      fatal("write failed");
    fclose(fd);
    return res;
  }

  return (long *)mmapfile(buf, &nres);
}
  
void usage()
{
  fatal("usage: cocitations X.int Y.int < pairs");
}

int count_dups(int *X, int n)
{
  int *end = X + n - 1;
  int res = 0;
  for( ;X<end;X++)
    if(X[0] == X[1]) {
      if(verbose) printf("intersect: %d\n", X[0]);
      res++;
    }
  return res;
}

int member(int x, int *X, int n)
{
  int *end = X+n;
  for( ;X<end; X++)
    if(x == *X) {
      if(verbose) printf("intersect: %d\n", x);
      return 1;
    }
  return 0;
}
  
int intersect(int *X, int Nx, int *Y, int Ny)
{
  if(Nx == 0 || Ny == 0) return 0;
  if(Ny == 1) return member(Y[0], X, Nx);
  if(Nx == 1) return member(X[0], Y, Ny);
  int N = Nx + Ny;
  int *tmp = malloc_ints(N);
  memcpy(tmp, X, Nx * sizeof(int));
  memcpy(tmp + Nx, Y, Ny * sizeof(int));
  qsort(tmp, N, sizeof(int), (__compar_fn_t)intcomp);
  int res = count_dups(tmp, N);
  free(tmp);
  return res;
}
  
void print_citations(int paper, int *citations, int n)
{
  int *end = citations+n;
  printf("%d (%d):", paper, n);
  for( ; citations<end; citations++)
    printf(" %d", *citations);
  printf("\n");
}

int main(int ac, char **av)
{
  // fprintf(stderr, "cocitations, calling main\n");

  if(ac < 3) usage();
  long Nx, Ny;
  
  int *X = (int *)mmapfile(av[1], &Nx);
  Nx /= sizeof(int);

  int *Y = (int *)mmapfile(av[2], &Ny);
  Ny /= sizeof(int);

  if(Nx != Ny) fatal("Nx != Ny");

  if(ac == 4 && strcmp(av[3], "--verbose") == 0) verbose++;

  // fprintf(stderr, "verbose = %d\n", verbose);

  // X is sorted, but Y is not
  // printf("X_order = %d\n", check_order(X, Nx));
  // printf("Y_order = %d\n", check_order(Y, Ny));

  long *idx = memoize_index(av[1], X, Nx);

  int paper[2];
  int ncitations[2];
  int *citations[2];
  int i;

  printf("paper1\tpaper2\tcitations1\tcitations2\tcocitations\n");

  while(scanf("%d%d", &paper[0], &paper[1]) == 2) {
    for(i=0;i<2;i++) {
      if(paper[i] < 0 || paper[i] >= Nx) fatal("bad input");
      citations[i] = Y + idx[paper[i]];
      ncitations[i] = idx[paper[i]+1] - idx[paper[i]];
      if(verbose) print_citations(paper[i], citations[i], ncitations[i]);
    }
    int cocitations = intersect(citations[0], ncitations[0], citations[1], ncitations[1]);
    printf("%d\t%d\t%d\t%d\t%d\n", paper[0], paper[1], ncitations[0], ncitations[1], cocitations);
  }
}
