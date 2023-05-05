#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>

int verbose = 0;

void usage()
{
  fatal("usage: calibrate_random_bytes_index random_bytes random_bytes.idx [N (number of bytes per record)] floats K [--stdin|--ascii|--binary] > report");
}

void *random_bytes;
long nrandom_bytes;

long N, K;

long *idx;
long nidx;

float *floats;
long nfloats;

/* long old_getlong(FILE *fd) */
/* { */
/*   long res; */
/*   if(fread(&res, sizeof(long), 1, fd) != 1) */
/*     fatal("getlong: read failed"); */
/*   return res; */
/* } */

// FILE *floats_fd, *random_bytes_fd, *idx_fd;

/* void old_get_floats(float *result, long offset, long n) */
/* { */
/*   long o = offset * n * sizeof(float); */
/*   if(verbose) fprintf(stderr, "get_floats: offset = %ld, o = %ld\n", offset, o); */
/*   if(fseeko64(floats_fd, o, SEEK_SET) != 0) { */
/*     fprintf(stderr, "errno = %d\n", errno); */
/*     perror("seek failed in get_floats"); */
/*     fatal("seek failed"); */
/*   } */
/*   if(fread(result, sizeof(float), n, floats_fd) != n) */
/*     fatal("fread failed"); */
/* } */

/* void old_get_random_bytes(void *result, long offset, long n) */
/* { */
/*   long o = offset * n * sizeof(char); */
/*   if(verbose) fprintf(stderr, "get_random_bytes: offset = %ld, o = %ld\n", offset, o); */
/*   if(fseeko64(random_bytes_fd, o, SEEK_SET) != 0) { */
/*     fprintf(stderr, "errno = %d\n", errno); */
/*     perror("seek failed in get_random_bytes"); */
/*     fatal("seek failed"); */
/*   } */
/*   if(fread(result, sizeof(char), n, random_bytes_fd) != n) */
/*     fatal("fread failed"); */
/* } */

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

int ASCII_MODE = 0;
int BINARY_MODE = 1;
int STDIN_MODE = 2;

int main(int ac, char **av)
{
  // char buf[1024];

  if(ac != 6 && ac != 7) usage();

  int mode=ASCII_MODE;

  if(ac == 7) {
    if(strcmp(av[ac-1], "--ascii") == 0) mode = ASCII_MODE;
    else if(strcmp(av[ac-1], "--binary") == 0) mode = BINARY_MODE;
    else if(strcmp(av[ac-1], "--stdin") == 0) mode = STDIN_MODE;
    else fatal("bad arg");
  }

  random_bytes = (void *)mmapfile(av[1], &nrandom_bytes);
  idx = (long *)mmapfile(av[2], &nidx);
  N = atoi(av[3]);        // length (in bytes) of record in random bytes
  floats = (float *)mmapfile(av[4], &nfloats);
  K = atoi(av[5]);	  // length (in floats) of record in floats

  if(verbose) fprintf(stderr, "N = %ld (length in bytes of record in random bytes: %s)\n", N, av[1]);
  if(verbose) fprintf(stderr, "K = %ld (length in floats of record in floats: %s)\n", K, av[4]);

  nrandom_bytes /= N * sizeof(char);
  nfloats /= K * sizeof(float);
  nidx /= sizeof(long);

  if(verbose) fprintf(stderr, "nrandom_bytes = %ld\n", nrandom_bytes);
  if(verbose) fprintf(stderr, "nfloats = %ld\n", nfloats);
  if(verbose) fprintf(stderr, "nidx = %ld\n", nidx);

  /* float *floats_buf = (float *)malloc(sizeof(float) * 2 * K); */
  /* void *random_bytes_buf  = (void *)malloc(sizeof(char) * 2 * N); */

  /* random_bytes_fd = fopen64(av[1], "r"); */
  /* if(!random_bytes_fd) { */
  /*   fprintf(stderr, "av[1] = %s\n", av[1]); */
  /*   fatal("open failed"); */
  /* } */

  /* floats_fd = fopen64(av[3], "r"); */
  /* if(!floats_fd) { */
  /*   fprintf(stderr, "av[3] = %s\n", av[3]); */
  /*   fatal("open failed"); */
  /* } */

  // sprintf(buf, "%s.idx", av[1]);

  /* idx_fd = fopen64(buf, "r"); */
  /* if(!idx_fd) { */
  /*   fprintf(stderr, "buf = %s\n", buf); */
  /*   fatal("open failed"); */
  /* } */

  if(!random_bytes || !idx) fatal("mmap failed");
  if(nidx != nrandom_bytes || nidx != nfloats) fatal("confusion");
  

  /* long prev_idx, cur_idx; */
  /* cur_idx = getlong(idx_fd); */

  /* get_floats(floats_buf + K, cur_idx,  K); */
  /* get_random_bytes(random_bytes_buf + N, cur_idx,  N); */

  long i;

  if(mode == STDIN_MODE)
    while(scanf("%ld", &i) == 1) {
      long prev_idx = idx[i-1];
      long cur_idx = idx[i];

      if(verbose) fprintf(stderr, "cur_idx = %ld\n", cur_idx);
      if(verbose) fprintf(stderr, "i=%d, idx[i-1]=%d, idx[i]=%d\n", i, prev_idx, cur_idx);
	printf("%06d\t%d\t%0.3f\t",
	       i,
	       hamming_dist(random_bytes + N * prev_idx, random_bytes + N * cur_idx, N),
	       cos_sim(floats + K * prev_idx, floats + K * cur_idx, K));
	hexify(random_bytes + N * cur_idx, N);
	putchar('\n');
      }

  else
    for(i=1; i<nidx ;i++) {
    
      long prev_idx = idx[i-1];
      long cur_idx = idx[i];

      if(verbose) fprintf(stderr, "cur_idx = %ld\n", cur_idx);

      /* memcpy(floats_buf, floats_buf+K, sizeof(float)*K); */
      /* get_floats(floats_buf + K, cur_idx, K); */

      /* memcpy(random_bytes_buf, random_bytes_buf+N, K); */
      /* get_random_bytes(random_bytes_buf + N, cur_idx,  N); */

      if(verbose) fprintf(stderr, "i=%d, idx[i-1]=%d, idx[i]=%d\n", i, prev_idx, cur_idx);
    
      /* printf("%06d\t%d\t%0.3f\t", */
      /* 	   i, */
      /* 	   hamming_dist(random_bytes_buf, random_bytes_buf + N, N), */
      /* 	   cos_sim(floats_buf, floats_buf+K, K)); */
      /* hexify(random_bytes_buf + N, N); */
      /* putchar('\n'); */

      if(mode==ASCII_MODE) {
	printf("%06d\t%d\t%0.3f\t",
	       i,
	       hamming_dist(random_bytes + N * prev_idx, random_bytes + N * cur_idx, N),
	       cos_sim(floats + K * prev_idx, floats + K * cur_idx, K));
	hexify(random_bytes + N * cur_idx, N);
	putchar('\n');
      }
      else {
	float sim = cos_sim(floats + K * prev_idx, floats + K * cur_idx, K);
	if(fwrite(&sim, sizeof(float), 1, stdout) != 1) fatal("write failed");
      }
    }
}
