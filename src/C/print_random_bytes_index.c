#include <stdio.h>
#include "util.h"
#include <memory.h>

void usage()
{
  fatal("usage: print_random_bytes_index random_bytes random_bytes.idx [N (number of bytes per record)] [--ascii|--binary] > report");
}

void *random_bytes;
long nrandom_bytes;
long N;

long *idx;
long nidx;

unsigned char hamming_dist1_memos[256][256] = {};


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

void hexify(long i)
{
  int j;
  // fprintf(stderr, "calling hexity[%d]\n", i);
  // fprintf(stderr, "idx[%d] = %d (max = %d)\n", i, idx[i], nrandom_bytes);

  unsigned char *bytes = random_bytes + idx[i] * N;
  for(j = 0;j<N;j++) 
    printf("%02x ", bytes[j]);
}

int ASCII_MODE = 0;
int BINARY_MODE = 1;

int main(int ac, char **av)
{
  // char buf[1024];

  init_hamming_dist1_memos();
  // fprintf(stderr, "memos initialized\n");

  int mode=ASCII_MODE;

  if(ac != 4 && ac != 5) usage();

  if(ac == 5) {
    if(strcmp(av[4], "--ascii") == 0) mode = ASCII_MODE;
    else if(strcmp(av[4], "--binary") == 0) mode = BINARY_MODE;
    else fatal("bad arg");
  }
       

  long i;
  N = atoi(av[3]);

  // fprintf(stderr, "N = %ld\n", N);

  random_bytes = (void *)mmapfile(av[1], &nrandom_bytes);
  nrandom_bytes /= N;

  // fprintf(stderr, "nrandom_bytes = %ld\n", nrandom_bytes);

  // sprintf(buf, "%s.idx", av[1]);
  idx = (long *)mmapfile(av[2], &nidx);
  nidx /= sizeof(long);

  // fprintf(stderr, "nidx = %ld\n", nidx);

  if(nidx != nrandom_bytes) fatal("confusion");

  if(mode == ASCII_MODE)
    for(i=1;i<nidx;i++) {
      printf("%06ld\t%10ld\t%d\t", i, idx[i],  hamming_dist(random_bytes + idx[i-1] *N, random_bytes + idx[i] *N, N));
      hexify(i);
      putchar('\n');
    }
  else if(mode == BINARY_MODE)
    for(i=1;i<nidx;i++) {
      unsigned int d = hamming_dist(random_bytes + idx[i-1] *N, random_bytes + idx[i] *N, N);
      if(d > 65535) d=65535;
      if(fwrite(&d, sizeof(short), 1, stdout) != 1)
	fatal("write failed");
    }
  else fatal("should not get here");
  
  exit(0);

}
