#include <stdio.h>
#include <stdlib.h>
#include "util.h"
#include <time.h>
#include <values.h>
// #include <openssl/rand.h>

void usage()
{
  fatal("usage: floats_to_random_bytes [K (number of floats per record)] [N (number of bytes per record)] [seed] < floats > bytes");
}


// some possibly useful summary statistics
long dot_calls = 0;
long dot_values = 0;

// input two vectors (a and b) of length n
// output the sign of the dot product of the two input vectors
int dot(float *a, float *b, int n)
{
  double res = 0;
  float *end = a+n;
  while(a<end)
    res += *a++ * *b++;

  int val = (res > 0);
  
  dot_calls++;
  dot_values += val;
  
  return val;
}

// F are some floats from an embedding with K hidden dimensions
// R are random floats of length 8*K

// output a byte (8 bits), where each bit is the sign of the dot
// product of the random vector with F

int do_it1(float *F, float *R, int K)
{
  int i = 0;
  int res = 0;
  for(i=0;i<8;i++,R+=K) 
    res = 2*res + dot(F, R, K);
  return res;
}
 
// input an embedding (floats) F
// R are random vectors of length 8*K
// the embedding has shape: (N, K)
// The output will be N bytes
void do_it(float *F, float *R, int K, int N)
{
  int i;
  for(i=0; i<N; i++,R+=8*K) {
    int byte = do_it1(F, R, K);
    putchar(byte);
  }
}

// want uniform random floats between -1 and 1
void init_random_floats(float *res, int n)
{
  float *end = res + n;
  double d = RAND_MAX/2.0;
  while(res < end)
    *res++ = rand()/d - 1.0;
}      

// Dead code -- we use the function above instead of this
// Not sure why, but this generates a non-uniform sample
void fancy_init_random_floats(float *res, int n)
{
  if(RAND_bytes((void *)res, sizeof(float) * n) != 1)
    fatal("random failed");

  float *end = res + n;
  double d = MAXINT;
  for(;res < end;res++)
    *res = ((int)(*res))/d;
}

int main(int ac, char **av)
{
  char *seed = NULL;
  if(ac == 3) srand(time(NULL));
  else if(ac == 4) seed = av[3];
  else usage();

  int K = atoi(av[1]);
  int N = atoi(av[2]);
  int K4 = K*4;

  if(seed) {
    fprintf(stderr, "seed = %s\n", seed);
    srand(atoi(seed));
  }
  else {
    int t = time(NULL);
    fprintf(stderr, "seed = NA (using time = %d to initialize seed)\n", t);
    srand(t);
  }

  fprintf(stderr, "floats_to_random_bytes: K = %d, N = %d\n", K, N);

  float *float_buffer = (float *)malloc(sizeof(float) * K);
  float *random_floats = (float *)malloc(sizeof(float) * K * N * 8);

  if(!float_buffer || !random_floats) fatal("malloc failed");
  
  init_random_floats(random_floats, K * N * 8);

  while(fread(float_buffer, K4, 1, stdin) == 1)
    do_it(float_buffer, random_floats, K, N);


  fprintf(stderr, "dot: %0.3f, vals = %ld, calls = %ld\n", dot_values/(double)dot_calls, dot_values, dot_calls);

  return 0;
}
