#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>

int verbose = 0;

void usage()
{
  fatal("usage: calibrate_random_bytes [K (floats per record)] [N (number of bytes per record)] floats random_bytes1 random_bytes2 ... < pairs > report");
}

void **random_bytes_files;
int nrandom_bytes_files;

long *Ns;

long N, K;

float *floats;
long nfloats;

double my_norm(float *x, int n)
{
  if(verbose) fprintf(stderr, "calling my_norm\n");
  double res = 0;
  float *end = x+n;
  for( ; x<end; x++)
    res += *x * *x;
  res = sqrt(res);
  if(verbose) fprintf(stderr, "my_norm --> %f\n", res);
  return res;
}

double my_dot(float *x, float *y, int n)
{
  if(verbose) fprintf(stderr, "calling my_dot\n");
  double res = 0;
  float *end = x+n;
  while(x<end)
    res += *x++ * *y++;
  if(verbose) fprintf(stderr, "my_dot --> %f\n", res);
  return res;
}

double cos_sim(float *a, float *b, int n)
{
  if(verbose) fprintf(stderr, "calling cos_sim\n");
  return my_dot(a, b, n)/(my_norm(a, n) * my_norm(b, n));  
}

int hamming_dist1(unsigned int a, unsigned int b)
{
  if(a == b) return 0;
  unsigned int i, result = 0;
  for(i=1;i<256;i*=2)
    if((a&i) != (b&i))
      result++;

  // printf("hamming_dist1[%03o, %03o] = %d\n", a&255, b&255, result);
  return result;
}
    
int hamming_dist(char *a, char *b, int n)
{
  if(verbose) fprintf(stderr, "calling hamming_dist\n");
  char *end = a + n;
  int result = 0;
  for( ; a<end; )
    result += hamming_dist1(*a++, *b++);
  if(verbose) fprintf(stderr, "hamming_dist --> %d\n", result);
  return result;
}

void hexify(unsigned char *bytes, int n)
{
  int j;
  for(j = 0;j<n;j++) 
    printf("%02x ", bytes[j]);
}

int main(int ac, char **av)
{

  if(ac < 5) usage();

  K = atoi(av[1]);	  // length (in floats) of record in floats
  N = atoi(av[2]);        // length (in bytes) of record in random bytes
  floats = (float *)mmapfile(av[3], &nfloats);

  int f;
  nrandom_bytes_files = ac-4;
  random_bytes_files = (void **)malloc(sizeof(void *) * nrandom_bytes_files);
  Ns = (long *)malloc(sizeof(long) * nrandom_bytes_files);
  if(!random_bytes_files || !Ns) fatal("malloc failed");
  
  for(f=0;f<nrandom_bytes_files;f++) {
    random_bytes_files[f] = (void *)mmapfile(av[f+4], &Ns[f]);
    // Ns[f] /= N;
    if(verbose) fprintf(stderr, "file %s has %ld records\n", av[f+4], Ns[f]/N);
  }

  if(verbose) fprintf(stderr, "N = %ld (length in bytes of record in random bytes: %s)\n", N, av[1]);
  if(verbose) fprintf(stderr, "K = %ld (length in floats of record in floats: %s)\n", K, av[4]);

  // nrandom_bytes /= N * sizeof(char);
  nfloats /= K * sizeof(float);

  // if(verbose) fprintf(stderr, "nrandom_bytes = %ld\n", nrandom_bytes);
  if(verbose) fprintf(stderr, "nfloats = %ld\n", nfloats);

  if(!floats) fatal("mmap failed");
  // if(nfloats != nrandom_bytes) fatal("confusion");

  long papers[2];
  while(scanf("%ld%ld", &papers[0], &papers[1]) == 2) {
    printf("%ld\t%ld\t%0.3f",
	   papers[0], papers[1],
	   cos_sim(floats + K * papers[0], floats + K * papers[1], K));
    for(f=0;f<nrandom_bytes_files;f++)
      if(N*papers[0] < Ns[f] && N*papers[1] < Ns[f])
	printf("\t%d", hamming_dist(random_bytes_files[f] + N * papers[0], random_bytes_files[f] + N * papers[1], N));
      else printf("\tNA[%ld]", Ns[f]);
    putchar('\n');
    fflush(stdout);

    // hexify(random_bytes + N * cur_idx, N);
    // putchar('\n');
  }

}
