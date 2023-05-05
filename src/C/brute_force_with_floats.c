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
  fatal("usage: echo new_paper_id | brute_force_with_floats [--record_size <n>] [--floats <file>] [--threshold 0] > report");
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

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}


int main(int ac, char **av)
{
  int i, j;
  int record_size = -1;
  float threshold = -2.0;
  FILE *fd = NULL;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--threshold") == 0) threshold = atof(av[++i]);
    else if(strcmp(av[i], "--floats") == 0) {
      char *fn = av[++i];
      floats = (float *)mmapfile(fn, &nfloats);
      nfloats /= sizeof(float);
      fd = fopen(fn, "rb");
      if(!fd) fatal("open failed");
    }
    else usage();
  }

  if(record_size <= 0) fatal("--record_size arg is required");

  // long new_paper_id = 7375270;
  long new_paper_id;

   while(scanf("%ld", &new_paper_id) == 1) {
     fseek(fd, 0, SEEK_SET);
     float *f = (float *)malloc(sizeof(float) * record_size);
     float *query = floats + new_paper_id * record_size;
     for(j=0; j*record_size < nfloats;j++) {
       // if(j > 10650966) fprintf(stderr,"j=%ld\n", j);
       if(fread(f, sizeof(float), record_size, fd) != record_size)
	 break;
       double d = my_cos(f, query, record_size);
       if(d > threshold)
	 printf("%f\t%ld\n", d, j);
    }
  }
}
