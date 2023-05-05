#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include "util.h"
#include <memory.h>

long *cumsum(long *X, long N)
{
  long i;
  long *res = (long *)malloc(sizeof(long) * N);
  res[0] = 0;
  for(i = 0; i<N; i++)
    res[i+1] = res[i] + X[i];
  return res;
}

long matrix_shape(struct bigram *M, long N)
{
  long res = 0;
  struct bigram *end = M + N;

  for( ;M < end; M++) {
    if(M->elts[0] >= res) res = M->elts[0]+1;
    if(M->elts[1] >= res) res = M->elts[1]+1;
  }
  fprintf(stderr, "matrix_shape --> %ld\n", res);
  return res;
}
 
long *index_bigrams(struct bigram *M, long N, long *n_index)
{
  fprintf(stderr, "calling index_bigrams\n");
  struct bigram *end = M + N;
  *n_index = matrix_shape(M, N);
  long *res = (long *)malloc(sizeof(long) * *n_index);
  memset(res, 0, sizeof(long) * *n_index);
  for( ; M < end; M++) {
    int e0 = M->elts[0];
    res[e0]++;
  }

  long *cres = cumsum(res, *n_index);
  (*n_index)++;

  fprintf(stderr, "index_bigrams: n_index = %ld\n", *n_index);
  return cres;
}

long *memoize_index(char *filename, struct bigram *table, long ntable, long *n_index)
{
  fprintf(stderr, "calling memoize_index: %s\n", filename);
  char buf[1024];
  sprintf(buf, "%s.idx", filename);
  FILE *fd = fopen(buf, "rb");
  long *res;
  if(!fd) {
    FILE *fd = fopen(buf, "wb");
    res = index_bigrams(table, ntable, n_index);
    if(fwrite(res, sizeof(long), *n_index, fd) != *n_index)
      fatal("write failed");
    fclose(fd);
    return res;
  }
  fclose(fd);
  res = (long *)mmapfile(buf, n_index);
  return res;
}
  
void usage()
{
  fatal("usage: echo 5 | x_to_y ai | extract_row bigrams");
}

int main(int ac, char **av)
{
  fprintf(stderr, "extract_row, calling main\n");

  if(ac != 2) usage();
  long N, n_index;
  struct bigram *b = (struct bigram *)mmapfile(av[1], &N);
  N /= sizeof(struct bigram);

  long *idx = memoize_index(av[1], b, N, &n_index);
  int x;

  while(fread(&x, sizeof(x), 1, stdin) > 0) {
    struct bigram *row = b + idx[x];
    long nrow = idx[x+1] - idx[x];
    fprintf(stderr, "query = %d, nrow = %ld\n", x, nrow);
    if(fwrite(row, sizeof(struct bigram), nrow, stdout) != nrow)
      fatal("write failed");
  }
}
