#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <math.h>
#include "util.h"

int verbose = 0;

void usage()
{
  fatal("usage: generate pairs of longs | killroy -tick <print debugging msgs every N records> -N <long> -M <memory size in GB> | outputs pairs of longs that are likely to be duplicated");
}

long primep(long x)
{
  long i, end = (long)sqrt((double)x);
  for(i=2;i<=end;i++)
    if((x/i)*i == x) return 0;
  return 1;
}
  
long find_prime(long x)
{
  long start = x;
  while(!primep(x)) x++;
  fprintf(stderr, "find_prime(%ld) -> %ld\n", start, x);
  return x;
}

long stats[128] = {0};

void print_stats_briefly()
{
  double Nstats = 0;
  int i;
  for(i=0;i<128;i++)
    Nstats += (double)stats[i];

  if(Nstats > 0)
    fprintf(stderr, "stats: 0: %0.5f, 1: %0.5f, 2: %0.5f, more: %0.5f\n",
	    stats[0]/Nstats,
	    stats[1]/Nstats,
	    stats[2]/Nstats,
	    (Nstats - stats[0] - stats[1] - stats[2])/Nstats);
}
 
void print_stats()
{
  double Nstats = 0;
  int i;
  for(i=0;i<128;i++)
    fprintf(stderr, "stats[%d] = %ld\n", i, stats[i]);
}


int main(int ac, char **av)
{
  long buf[2];
  int i;
  long N = -1;
  double M = -1.0;
  long filled=0;
  long input_records = 0;
  long output_records = 0;
  long tick = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--verbose") == 0) verbose++;
    else if(strcmp(av[i], "-N") == 0) N = atol(av[++i]);
    else if(strcmp(av[i], "-M") == 0) M = atof(av[++i]);
    else if(strcmp(av[i], "-tick") == 0) tick = atol(av[++i]);
    else usage();
  }

  fprintf(stderr, "killroy: M = %f, N = %ld, tick = %ld\n", M, N, tick);

  if(M < 0 || N < 0) usage();

  long P = find_prime((long)(M * 1e9));
  long too_full = P/2;
  long table_size = P;
  char *table = (char *)malloc(table_size);
  if(!table) fatal("malloc failed");
  memset(table, 0, table_size);

  while(fread(buf, sizeof(long), 2, stdin) == 2) {
    if(tick > 0 && input_records++ % tick == 0) {
      double used = (double)filled/(double)P;
      double in_out_ratio = 0;
      
      if(output_records > 0) in_out_ratio = input_records/(double)output_records;
      fprintf(stderr, "killroy: %d M input records, %0.1f in/out ratio, filled = %f of %ld\n", input_records/1000000, in_out_ratio, used, P);
      print_stats_briefly();
    }

    long a = buf[0];
    long b = buf[1];
    if(a > b) {
      a = buf[1];
      b = buf[0];
    }
    long offset = (a * N + b) % P;
    if(offset <= 0) offset += P;

    if(table[offset] == 0) {
      if(filled++ >= too_full) {
	fprintf(stderr, "killroy: cleanning house\n");
	filled=0;
	memset(table, 0, table_size);
      }
    }
    
    // output only when you go from zero to one
    // but that can miss stuff with hash collisions
    if(table[offset] >= 1) {
      buf[0] = a;
      buf[1] = b;
      output_records++;
      if(fwrite(buf, sizeof(long), 2, stdout) != 2)
	fatal("write failed");
    }

    // don't wrap around
    int c = table[offset];
    if(c < 128) {
      table[offset]++;
      stats[c]++;
    }
    else stats[127]++;
  }

  print_stats();
  return 0;
}
