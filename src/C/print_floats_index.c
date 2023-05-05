#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>

void usage()
{
  fatal("usage: print_floats_index floats idx [N (number of bytes per record)] [--ascii|--binary] > report");
}

float *floats;
long nfloats;
long N;

long *idx;
long nidx;

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
  return dot(a, b, n)/(alen * blen);
}

int ASCII_MODE = 0;
int BINARY_MODE = 1;

int main(int ac, char **av)
{

  int mode=ASCII_MODE;

  if(ac != 4 && ac != 5) usage();

  if(ac == 5) {
    if(strcmp(av[4], "--ascii") == 0) mode = ASCII_MODE;
    else if(strcmp(av[4], "--binary") == 0) mode = BINARY_MODE;
    else fatal("bad arg");
  }
       

  long i;
  N = atoi(av[3]);

  floats = (void *)mmapfile(av[1], &nfloats);
  nfloats /= N * sizeof(float);

  idx = (long *)mmapfile(av[2], &nidx);
  nidx /= sizeof(long);

  if(nidx != nfloats) fatal("confusion");

  if(mode == ASCII_MODE)
    for(i=1;i<nidx;i++) {
      printf("%06d\t%10d\t%d\n", i, idx[i],  my_cos(floats + idx[i-1] *N, floats + idx[i] *N, N));
    }
  else if(mode == BINARY_MODE)
    for(i=1;i<nidx;i++) {
      float d = my_cos(floats + idx[i-1] *N, floats + idx[i] *N, N);
      if(fwrite(&d, sizeof(float), 1, stdout) != 1)
	fatal("write failed");
    }
  else fatal("should not get here");
  
  exit(0);

}
