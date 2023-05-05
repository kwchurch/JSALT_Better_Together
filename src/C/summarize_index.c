#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>

void usage()
{
  fatal("usage: summarize_index --index --floats --random_bytes --record_size --piece --npieces --max_offset > report");
}

void *random_bytes;
long nrandom_bytes;
long N;

long *idx;
long nidx;

unsigned char hamming_dist1_memos[256][256] = {};

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

void init_hamming_dist1_memos()
{
  int i,j;
  for(i=0;i<=256;i++)
    for(j=0;j<=256;j++)
      hamming_dist1_memos[i][j]=hamming_dist1(i,j);
}
    
int hamming_dist(unsigned char *a, unsigned char *b, int n)
{
  unsigned char *end = a + n;
  int result = 0;
  for( ; a<end; )
    result += hamming_dist1_memos[*a++][*b++];
  return result;
}

int main(int ac, char **av)
{
  int i, piece, npieces, record_size, max_offset = 1;
  float *floats = NULL;
  void *random_bytes = NULL;
  long *idx = NULL;
  long nfloats, nrandom_bytes, nidx;
  record_size = piece = npieces = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--floats") == 0) {
      floats = (float *)mmapfile(av[++i], &nfloats);
      nfloats /= sizeof(float);
    }
    else if(strcmp(av[i], "--index") == 0) {
      idx = (long *)mmapfile(av[++i], &nidx);
      nidx /= sizeof(long);
    }
    else if(strcmp(av[i], "--random_bytes") == 0) {
      random_bytes = (void *)mmapfile(av[++i], &nrandom_bytes);
      init_hamming_dist1_memos();
      fprintf(stderr, "memos initialized\n");
    }
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--piece") == 0) piece = atoi(av[++i]);
    else if(strcmp(av[i], "--npieces") == 0) npieces = atoi(av[++i]);
    else if(strcmp(av[i], "--max_offset") == 0) max_offset = atoi(av[++i]);
    else {
      fprintf(stderr, "av[%d] = %s\n", i, av[i]);
      usage();
    }
  }
	
  if(!idx) fatal("--index arg is required");
  if(record_size < 0) fatal("--record_size arg is required");
  if(piece < 0) fatal("--piece arg is required");
  if(npieces < 0) fatal("--npieces arg is required");
  if(piece >= npieces) fatal("bad arg --piece");

  int j, offset;
  long start = piece * nidx/npieces;
  long end = (piece+1) * nidx/npieces;

  if((piece+1) >= npieces) end = nidx;

  // fprintf(stderr, "start = %ld, end = %ld\n", start, end);

  if(random_bytes) 
    for(j=start;j<end;j++) {
      printf("%ld", j);
      for(offset=1;offset<=max_offset;offset++) {
	unsigned int d = 65535;
	if(j-offset >= 0) d = hamming_dist(random_bytes + idx[j-offset] * record_size, random_bytes + idx[j] * record_size, record_size);  
	if(d > 65535) d=65535;
	printf("\t%d", d);
      }
      putchar('\n');
    }
  else if(floats) {
    double d;
    for(j=start;j<end;j++) {
      printf("%ld", j);
      for(offset=1;offset<=max_offset;offset++) {
	if(j-offset >= 0) d = my_cos(floats + idx[j-offset] * record_size, floats + idx[j] * record_size, record_size);
	else d = -1.0;
	printf("\t%f", j, d);
      }
      putchar('\n');
    }
  }
  else fatal("must specify either --random_bytes or --floats");
  
  exit(0);

}
