#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <strings.h>
#include "util.h"
#include <search.h>

int verbose = 20; 

int *malloc_ints(int n)
{
  int *result = (int *)malloc(sizeof(int) * n);
  if(!result) fatal("malloc failed");
  memset(result, 0, sizeof(int) * n); /* not necessary, but safer...  */
  return result;
}

int *permutation, *ipermutation;
long int npermutation;

void invert_permutation()
{
  int i;
  ipermutation = malloc_ints(npermutation);
  for(i=0;i<npermutation;i++)
    ipermutation[permutation[i]] = i;
}

void check_permutation()
{
  int i;
  for(i=0;i<npermutation;i++)
    if(i != ipermutation[permutation[i]] ||
       i != permutation[ipermutation[i]]) {
      fprintf(stderr, "i = %d\n", i);
      fatal("check_permutation");
    }
}
      
void check_order(int *X, int n)
{
  int *Xend = X + n;
  X++;
  for( ; X < Xend; X++)
    if(X[-1] > X[0])
      fatal("check_order failed");
}

int freq(int *X, int *Xend)
{
  int *base = X;
  
  for( ; X < Xend; X++)
    if(*X != *base)
      break;
  
  int res = X-base;
  // fprintf(stderr, "freq returning %d\n", res);
  return res;
}

void usage()
{
  fprintf(stderr, "usage: freq_row_piece input output permutation T\n");
  fprintf(stderr, "\tinput and output are pairs of files with suffixes .X and .Y\n");
  fprintf(stderr, "\tT is a threshold on freq for sketching, typically 100\n");
  fatal("usage");
}

/* def ksmallest(vals, k): */
/*     n = len(vals) */
/*     if n < 2*k: */
/*         return np.sort(vals)[0:k] */
/*     else: */
/*         lo = np.min(vals) */
/*         hi = np.max(vals) */
/*         r = hi - lo */
/*         mid = lo + (1.1 * r)/k */
/*         s = vals < mid */
/*         if np.sum(s) >= k: */
/*             return ksmallest(vals[s], k) */
/*         else: */
/*             return np.sort(vals)[0:k] */

void check_row(int *row, int n)
{
  int *end = row + n;
  while(row < end) {
    int x = *row++;
    if(x < 0 || x >= npermutation) fatal("confusion in check_row");
  }
}

int *permute_row(int *result, int *row, int n)
{
  // This invariant does not hold
  // check_row(row, n);
  // int *result = malloc_ints(n);

  int *base = result;
  if(verbose > 10) fprintf(stderr, "permute_row: n = %d\n", n);

  int *end = row + n;
  while(row < end)
    *result++ = permutation[*row++];

  return base;
}

// inverse of above
int *ipermute_row(int *result, int *row, int n)
{
  // This invariant does not hold
  // check_row(row, n);
  // check_row(row, n);
  // int *result = malloc_ints(n);
  int *base = result;
  if(verbose > 10) fprintf(stderr, "ipermute_row: n = %d\n", n);
  int *end = row + n;
  for(; row < end; )
    *result++ = ipermutation[*row++];
  return base;
}

int permute(int a)
{
  if(a < 0 || a >= npermutation)
    fatal("confusion in permute");
  return permutation[a];
}

int find_min_with_permute(int *vals, int n)
{
  int *end = vals + n;
  int result = *vals++;
  for( ; vals < end; vals++)
    if(permute(*vals) < result) result = *vals;
  return result;
}

int find_max_with_permute(int *vals, int n)
{
  int *end = vals + n;
  int result = *vals++;
  for( ; vals < end; vals++)
    if(permute(*vals) > result) result = *vals;
  return result;
}

int count_below_with_permute(int *vals, int n, int T, int enough)
{
  int *end = vals + n;
  int result = 0;
  for( ; vals < end && result < enough; vals++)
    if(permute(*vals) <= T) result++;
  return result;
}

int copy_below_with_permute(int *buf, int *vals, int n, int T)
{

  int *end = vals + n;
  int result = 0;
  for( ; vals < end; vals++)
    if(permute(*vals) <= T) buf[result++] = *vals;
  return result;
}

int intcomp_with_permute(int *a, int*b)
{
  if(*a < 0 || *b < 0 || *a >= npermutation || *b >= npermutation)
    fatal("confusion in permutation_intcomp");

  int pa = permutation[*a];
  int pb = permutation[*b];
  if(pa < pb) return -1;
  if(pa > pb) return 1;
  return 0;
}

int find_min(int *vals, int n)
{
  int *end = vals + n;
  int result = *vals++;
  for( ; vals < end; vals++)
    if(*vals < result) result = *vals;
  return result;
}

int find_max(int *vals, int n)
{
  int *end = vals + n;
  int result = *vals++;
  for( ; vals < end; vals++)
    if(*vals > result) result = *vals;
  return result;
}

// min and max are return values
int find_range(int *vals, int n, int *min, int *max)
{
  int *end = vals + n;
  *min = *max = *vals++;

  for( ; vals < end; vals++) {
    if(*vals < *min) *min = *vals;
    if(*vals > *max) *max = *vals;
  }
  return *max - *min;
}  

int count_below(int *vals, int n, int T, int enough)
{
  int *end = vals + n;
  int result = 0;
  for( ; vals < end && result < enough; vals++)
    if(*vals <= T) result++;
  return result;
}

int copy_below(int *buf, int *vals, int n, int T)
{

  int *end = vals + n;
  int result = 0;
  for( ; vals < end; vals++)
    if(*vals <= T) buf[result++] = *vals;
  return result;
}

int intcomp(int *a, int*b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

int *ksmallest_endgame(int *result, int nresult, int *vals, int nvals, int k)
{
  if(verbose > 10) fprintf(stderr, "calling ksmallest_endgame ... ");  
  /* do not expect this to happen, but just being safe */
  if(nvals < k)
    memset(result, 0, sizeof(int) * k);

  if(nvals < nresult) {
    memcpy(result, vals, sizeof(int) * nvals );
    qsort(result, nvals, sizeof(int), (__compar_fn_t)intcomp);
    if(verbose > 10) fprintf(stderr, "leaving ksmallest_endgame\n");  
    return result;
  }
}

int *ksmallest(int *result, int nresult, int *vals, int nvals, int k)
{
  int lo,hi;

  if(verbose > 10) fprintf(stderr, "calling ksmallest ... ");  
  if(nvals < nresult)
    return ksmallest_endgame(result, nresult, vals, nvals, k);
    
  int range = find_range(vals, nvals, &lo, &hi);

  if(verbose > 10) fprintf(stderr, "range: lo = %d, hi = %d; nvals = %d\n", lo, hi, nvals);

  while(lo < hi) {
    int mid = lo + (hi-lo)/2;
    int c = count_below(vals, nvals, mid, nresult+1);
    if(verbose > 10) if(verbose) fprintf(stderr, "found %d values below %d between %d and %d\n", c, mid, lo, hi);

    if(c >= k && c < nresult) {
      nresult = copy_below(result, vals, nvals, mid);
      qsort(result, nresult, sizeof(int), (__compar_fn_t)intcomp);
      if(verbose > 10) fprintf(stderr, "leaving ksmallest\n");  
      return result;
    }
    if(c < k) lo = mid;
    else hi = mid;
  }
  
  // This should not happen
  fprintf(stderr, "Something is wrong in ksmallest; doing it the hardway for nvals = %d\n", nvals);
  int *buf = malloc_ints(nvals);
  memcpy(buf, vals, sizeof(int) * nvals);
  qsort(buf, nvals, sizeof(int), (__compar_fn_t)intcomp);
  memcpy(result, buf,sizeof(int) * k);
  free(buf);
  return result;
}
    
void my_output(FILE **outf, int *X, int *Y, int n)
{
  if(verbose > 10) fprintf(stderr, "calling my_output ... ");
  if(fwrite(X, sizeof(int), n, outf[0]) != n) fatal("write failed");
  // fflush(outf[0]);
  if(fwrite(Y, sizeof(int), n, outf[1]) != n) fatal("write failed");
  // fflush(outf[1]);
  if(verbose > 10) fprintf(stderr, "done.\n");
}

int main(int ac, char **av)
{
  char filenames[5][1024];

  if(ac != 5) usage();

  permutation = (int *)mmapfile(av[3], &npermutation);
  npermutation /= sizeof(int);
  sprintf(filenames[4], "%sinv", av[3]);
  ipermutation = (int *)mmapfile(filenames[4], &npermutation);
  npermutation /= sizeof(int);

  /* This should not be necessary */
  /* fprintf(stderr, "checking permutation ... "); */
  /* check_permutation(); */
  /* fprintf(stderr, "done.\n"); */

  /* fprintf(stderr, "inverting permutation ... "); */
  /* invert_permutation();   */
  /* fprintf(stderr, "done.\n"); */

  int T = atoi(av[4]);
  fprintf(stderr, "T = %d\n", T);

  char *Xfilename = filename(filenames[0], av[1], "X");
  char *Yfilename = filename(filenames[1], av[1], "Y");

  FILE *outf[2];

  outf[0]= fopen(filename(filenames[2], av[2], "sketch.X"), "wb");
  outf[1]= fopen(filename(filenames[3], av[2], "sketch.Y"), "wb");

  long int nX, nY;
  int *X = (int *)mmapfile(Xfilename, &nX);
  int *Y = (int *)mmapfile(Yfilename, &nY);
  nX /= sizeof(int);
  nY /= sizeof(int);
  int *Xend = X + nX;
  int *Yend = Y + nY;

  fprintf(stderr, "nX = %ld; nY = %ld; npermutation = %ld\n", nX, nY, npermutation);
  if(nX != nY) fatal("expected nX == nY");

  if(X == NULL || Y == NULL) fatal("mmap failed");

  fprintf(stderr, "checking order  ... ");
  check_order(X, nX);
  fprintf(stderr, "done.\n");

  // make buf 20% larger than necessary
  int nbuf = 5*T/4;
  int *buf = (int *)malloc_ints(nbuf);
  int *ip_buf = (int *)malloc_ints(T);
  if(buf == NULL || ip_buf == NULL) fatal("malloc failed");
  int p, freqp;

  int *row_buf = NULL;
  int nrow_buf = -1;

  for(p=0 ; p<nX; p+=freqp) {
    // fprintf(stderr, "p=%d\n",  p);
    freqp = freq(X+p, Xend);
    fprintf(stderr, "p=%d, X[p]=%d, freq=%d\n",  p, X[p], freqp);
    if(freqp < T) fatal("confusion");

    if(freqp > nrow_buf) {
      if(row_buf) free(row_buf);
      row_buf = malloc_ints(freqp);
      nrow_buf = freqp;
      fprintf(stderr, "p = %d, nrow_buf = %d\n", p, nrow_buf);
    }

    int *prow = permute_row(row_buf, Y+p, freqp);
    // int *smallest = ksmallest(buf, nbuf, Y+p, freqp, T);
    int *smallest = ksmallest(buf, nbuf, prow, freqp, T);
    int *result = ipermute_row(ip_buf, smallest, T);
    // int *result = smallest;
    my_output(outf, X+p, result, T);
  }
}
