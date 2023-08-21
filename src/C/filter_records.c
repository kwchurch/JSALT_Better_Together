#include <stdio.h>
#include <memory.h>
#include <stdlib.h>
#include <math.h>
#include "util.h"

int verbose = 0;

void usage()
{
  fatal("usage: cat records | filter_records --tick <records between debugging msgs> --count_flag --dtype L --record_size <bytes> --good_records <filename>  | outputs records in good file");
}

long tick = -1;
int record_size = 0;
char *good_records = NULL;
long ngood_records = 0;

int record_compare(char *a, char *b) {
  return memcmp(a, b, record_size);
}
  
int main(int ac, char **av)
{
  int i;
  char *dtype = "L";
  int count_flag = 0;
  long input_records = 0;
  long matches = 0;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--help") == 0) usage();
    else if(strcmp(av[i], "--verbose") == 0) verbose++;
    else if(strcmp(av[i], "--record_size") == 0) record_size = atoi(av[++i]);
    else if(strcmp(av[i], "--good_records") == 0) good_records = (char *)readchars(av[++i], &ngood_records);
    else if(strcmp(av[i], "--dtype") == 0) dtype = av[++i];
    else if(strcmp(av[i], "--count_flag") == 0) count_flag=1;
    else if(strcmp(av[i], "--tick") == 0) tick = atol(av[++i]);
    else usage();
  }

  if(record_size <= 0 || ngood_records <= 0) usage();

  ngood_records /= record_size;

  fprintf(stderr, "record_size = %d\n", record_size);
  fprintf(stderr, "ngood_records = %ld\n", ngood_records);

  qsort(good_records, ngood_records, record_size, record_compare);

  fprintf(stderr, "qsort done\n");

  char *buf = (char *)malloc(record_size);
  if(!buf) fatal("malloc failed");

  // without count_flag option, simply output records in good_records (in binary)
  if(count_flag == 0) {
    while(fread(buf, record_size, 1, stdin) == 1) {
      if(bsearch(buf, good_records, ngood_records, record_size, record_compare) != NULL) {
	matches++;
	if(fwrite(buf, record_size, 1, stdout) != 1)
	  fatal("write failed");
      }
    }

    if(tick > 0 && input_records % tick == 0)
      fprintf(stderr, "filter_records: records = %0.1f million, matches = %ld (match rate = %f)\n",
	      (double)input_records/1000000.0, matches, matches/(double)input_records);
  }

  // with count_flag option, create a report (in ascii)
  // with counts of matches of each record in good records with records in stdin
  else {

    if(strcmp(dtype, "L") != 0) fatal("currently supported dtypes: L");
    long *counts = (long *)malloc(sizeof(long) * ngood_records);
    if(!counts) fatal("malloc failed");
    memset(counts, 0, sizeof(long) * ngood_records);
      
    while(fread(buf, record_size, 1, stdin) == 1) {
      input_records++;
      char *found = (char *)bsearch(buf, good_records, ngood_records, record_size, record_compare);
      if(found != NULL) {
	matches++;
	counts[(found - good_records)/record_size]++;
      }

      if(tick > 0 && input_records % tick == 0) 
	fprintf(stderr, "filter_records: records = %0.1f million, matches = %ld (match rate = %f)\n",
		(double)input_records/1000000.0, matches, matches/(double)input_records);
    }
    
    long j, k;
    for(j=0;j<ngood_records;j++) {
      printf("%ld", counts[j]);
      long *rec = (long *)(good_records + j * record_size);
      for(k=0;k<record_size/sizeof(long);k++)
	printf("\t%ld", rec[k]);
      printf("\n");
    }
  }
}
