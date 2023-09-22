#include <stdio.h>
#include <stdlib.h>
#include "util.h"
#include <time.h>
#include <limits.h>
#include <math.h>

void usage()
{
  fatal("usage: center_floats [K (record size)] floats > new_floats");
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

void normalize(float *a, int n)
{
  float *aend = a + n;
  double an = norm(a, n);
  if(an < SMALL) return;
  while(a < aend)
    *a++ /= an;
}

void *my_sum(float *res, float *F, int K)
{
  float *end = res + K;
  for( ; res<end; res++,F++)
    *res += *F;
}

float *get_center(float *F, int K, long nfloats)
{
  float *end = F + nfloats;
  float *res = (float *)malloc(sizeof(float) * K);
  memset(res, 0, sizeof(float) * K);
  
  for( ; F < end; F += K)
    my_sum(res, F, K);

  int i;
  double n = nfloats/K;
  for(i=0;i<K;i++)
    res[i] /= n;

  return res;
}

float *center_vec(float *buf, float *F, float *center, int K)
{
  int i;
  memcpy(buf, F, sizeof(float) * K);
  for(i=0;i<K;i++)
    buf[i] -= center[i];

  normalize(buf, K);
  return buf;
}

void print_center(FILE *fd, float *center, int K)
{
  int i;
  for(i=0; i<K; i++)
    fprintf(stderr, "center[%d] = %0.5f\n", i, center[i]);
}
 
int main(int ac, char **av)
{

  if(ac != 3) usage();

  int K = atoi(av[1]);
  long nfloats;

  float *floats = (float *)mmapfile(av[2], &nfloats);
  nfloats /= sizeof(float);

  fprintf(stderr, "center_floats: K = %d, nfloats = %ld\n", K, nfloats);

  float *center = get_center(floats, K, nfloats);

  print_center(stderr, center, K);

  float *buf = (float *)malloc(sizeof(float) * K);
  if(!buf) fatal("malloc failed");

  fprintf(stderr, "center_floats (pt2): K = %d, nfloats = %ld\n", K, nfloats);
  float *F = floats;
  float *end = F + nfloats;
  for( ; F < end; F += K) {
    if(fwrite(center_vec(buf, F, center, K), sizeof(float), K, stdout) != K)
      fatal("write failed");
  }

  return 0;
}
