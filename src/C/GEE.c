#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fatal("usage: GEE (Graph Embedding Encoder) X0 X1 X2 Y > Z");
}

int my_max(int *vec, long n)
{
  int *end = vec + n;
  int res = vec[0];
  for(; vec<end; vec++)
    if(*vec > res) res=*vec;
  return res;
}

int *bincount(int *vec, long n, long *nres)
{
  int *end = vec + n;
  *nres = my_max(vec, n)+1;
  int *res = (int *)malloc(sizeof(int) * *nres);
  if(!res) fatal("malloc failed");
  memset(res, 0, sizeof(int) * *nres);
  for(; vec<end;vec++)
    res[*vec]++;
  return res;
}


int main(int ac, char **av)
{
  long nX0, nX1, nX2;
  long s;			/* number of edges (X values) */
  long k;			/* number of hidden dimensions */
  long n;			/* number of labels (Y values) */

  if(ac != 5) usage();
  
  int *X0 = (int *)mmapfile(av[1], &nX0);
  nX0 /= sizeof(int);
  int *X1 = (int *)mmapfile(av[2], &nX1);
  nX1 /= sizeof(int);

  float *X2 = (float *)mmapfile(av[3], &nX2);
  nX2 /= sizeof(float);

  if(nX0 != nX1 || nX0 != nX2) fatal("assertion failed");
  s = nX0;

  int *Y = (int *)mmapfile(av[4], &n);
  n /= sizeof(int);  

  int *X0end = X0 + s;
  int *nk = bincount(Y, n, &k);

  /* float *nk2 = (float *)malloc(sizeof(float) * n); */
  /* if(!nk2) fatal("malloc failed"); */
  /* int i; */
  /* for(i=0;i<n;i++) nk2[i] = nk[Y[i]]; */

  fprintf(stderr, "s (edges) = %ld, n = %ld, k = %ld\n", s, n, k);
  
  float *Z = (float *)malloc(sizeof(float) * n * k);
  if(!Z) fatal("malloc failed");

  memset(Z, 0, sizeof(float) * n * k);

  // fprintf(stderr, "pt1\n");

  for(;X0 < X0end; X0++,X1++,X2++) {
    int v_i = *X0;
    int v_j = *X1;

    if(v_i < 0 || v_i >= n) fatal("assertion failed");
    if(v_j < 0 || v_j >= n) fatal("assertion failed");

    int label_i = Y[v_i];
    int label_j = Y[v_j];
    
    if(label_i < 0 || label_i >= k) fatal("assertion failed");
    if(label_j < 0 || label_j >= k) fatal("assertion failed");
    
    // fprintf(stderr, "edge: %d, %d; labels = %d, %d\n", v_i, v_j, label_i, label_j);

    Z[v_i *k + label_j ] += *X2/(double)nk[label_j];
    if(v_i != v_j)
      Z[v_j*k + label_i] += *X2/(double)nk[label_i];
  }

  if(fwrite(Z, sizeof(float), n*k, stdout) != n*k)
    fatal("write failed");
}
