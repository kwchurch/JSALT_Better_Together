#include <stdio.h>
#include <stdlib.h>
#include "util.h"
#include <time.h>
// #include <values.h>
#include <limits.h>
#include <math.h>
// #include <openssl/rand.h>

void usage()
{
  fatal("usage: floats_to_random_bytes_stats --dir dir --seed seed < ids");
}


// int sample_size = 1000;
int record_size = -1;
int random_bytes = -1;
float *floats = NULL;
long nfloats;


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

void get_args_from_dir(char *dir)
{
  fprintf(stderr, "get_args_from_dir: %s\n", dir);
  char buf[1024];
  sprintf(buf, "%s/record_size", dir);

  FILE *fd = fopen(buf, "r");
  fscanf(fd, "%d", &record_size);
  fprintf(stderr, "record_size: %d\n", record_size);
  fgets(buf, 1024, fd);
  fscanf(fd, "%d", &random_bytes);
  fprintf(stderr, "random_bytes: %d\n", random_bytes);
  fclose(fd);
  
  sprintf(buf, "%s/embedding.f", dir);
  floats = (float *)mmapfile(buf, &nfloats);
  nfloats /= sizeof(float);

  // sprintf(buf, "%s/map", dir);
  // init_node_map(buf);
  fprintf(stderr, "leaving, get_args_from_dir: %s\n", dir);
}    

int main(int ac, char **av)
{
  int i;
  char *seed = NULL;
  // srand(time(NULL));
  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--dir") == 0) get_args_from_dir(av[++i]);
    else if(strcmp(av[i], "--seed") == 0) seed = av[++i];
    // else if(strcmp(av[i], "--sample_size") == 0) samplesize = atoi(av[++i]);
    else if(strcmp(av[i], "--help") == 0) usage();
    else usage();
  }

  if(!floats) usage();

  if(seed) {
    fprintf(stderr, "seed = %s\n", seed);
    i = atoi(seed);
    srand(i);
  }
  else {
    int t = time(NULL);
    fprintf(stderr, "seed = NA (using time = %d to initialize seed)\n", t);
    srand(t);
  }

  int K = record_size;
  int B = random_bytes;
  float *float_buffer = (float *)malloc(sizeof(float) * K);
  float *random_floats = (float *)malloc(sizeof(float) * K * B * 8);

  if(!float_buffer || !random_floats) fatal("malloc failed");
  
  init_random_floats(random_floats, K * B * 8);

  /* if(fwrite(random_floats, sizeof(float), K * B * 8, stdout) != K * B * 8) */
  /*   fatal("write failed"); */

  /* return 0; */

  // JUST ADDED...
  for(i=0;i<K*B*8; i+=K)
    normalize(random_floats + i, K);

  long new_paper_id;

  while(scanf("%ld", &new_paper_id) == 1) {
    memcpy(float_buffer, floats + K * new_paper_id, K * sizeof(float));
    normalize(float_buffer, K);
    do_it(float_buffer, random_floats, K, B);
  }

  fprintf(stderr, "dot: %0.3f, vals = %ld, calls = %ld\n", dot_values/(double)dot_calls, dot_values, dot_calls);

  return 0;
}
