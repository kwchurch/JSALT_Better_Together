#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "util.h"

void usage()
{
  fprintf(stderr, "usage: invert_landmarks --docs start,end --number_of_landmarks 100 --input_landmarks landmarks.i --output_postings postings  --tick 100\n");
  fatal("usage");
}

int my_max(int *vec, long n)
{
  int result = *vec;
  int *end = vec + n;
  for(; vec<end;vec++)
    if(*vec > result) result=*vec;
  return result;
}

int my_min(int *vec, long n)
{
  int result = *vec;
  int *end = vec + n;
  for(; vec<end;vec++)
    if(*vec < result) result=*vec;
  return result;
}



int *hist(int *vec, long N, long *nhist)
{
  int minv = my_min(vec, N);
  int maxv = my_max(vec, N);
  
  if(minv < 0) fatal("hist: expected array to have no values less than 0");

  int n = 1+my_max(vec, N);
  *nhist = n;
  
  int *result = (int *)malloc(sizeof(int) * n);
  if(!result) fatal("malloc failed");
  memset(result, 0, sizeof(int)*n);
  int *end = vec+N;
  for(;vec<end;vec++)
    result[*vec]++;
  return result;
}

long *cumhist(int *hist, long N)
{
  long i;
  long *result = (long *)malloc(sizeof(long) * N);
  if(!result) fatal("cumhist: malloc failed");

  *result = hist[0];
  for(i=1;i<N;i++)
    result[i] = result[i-1] + hist[i];
  return result;
}

void output_longs(long *longs, long n, char *fn)
{
  fprintf(stderr, "output_longs: n = %ld, fn = %s\n", n, fn);

  FILE *fd = fopen(fn, "wb");
  if(!fd) fatal("open failed");
  if(fwrite(longs, sizeof(long), n, fd) != n)
    fatal("write failed");
  fclose(fd);
}

void output_ints(int *ints, long n, char *fn)
{
  fprintf(stderr, "output_ints: n = %ld, fn = %s\n", n, fn);

  FILE *fd = fopen(fn, "wb");
  if(!fd) fatal("open failed");
  if(fwrite(ints, sizeof(int), n, fd) != n)
    fatal("write failed");
  fclose(fd);
}

int main(int ac, char **av)
{
  int tick = -1;
  int i, j;
  char filename_buf[256];
  int number_of_landmarks = 0;
  int *landmarks = NULL;
  char *postings = NULL;
  long nlandmarks;
  int docs_start = 0;
  int docs_end = -1;

  for(i=1;i<ac;i++) {
    if(strcmp(av[i], "--number_of_landmarks") == 0) number_of_landmarks = atoi(av[++i]);
    else if(strcmp(av[i], "--input_landmarks") == 0) {
      landmarks = (int *)mmapfile(av[++i], &nlandmarks);
      nlandmarks /= sizeof(int);
    }
    else if(strcmp(av[i], "--output_postings") == 0) postings = av[++i];
    else if(strcmp(av[i], "--tick") == 0) tick = atoi(av[++i]);
    else if(strcmp(av[i], "--docs") == 0) sscanf(av[++i], "%d,%d", &docs_start, &docs_end);
    else {
      fprintf(stderr, "i=%d, av[i] = %s\n", i, av[i]);
      usage();
    }
  }

  if(!postings) {
    fprintf(stderr, "--postings arg is required\n");
    usage();
  }

  if(!landmarks) {
    fprintf(stderr, "--landmarks arg is required\n");
    usage();
  }

  if(!number_of_landmarks) {
    fprintf(stderr, "--number_ob_landmarks arg is required\n");
    usage();
  }

  long *cumH;
  long nH=0;

  char *cumhist_file = filename(filename_buf, postings, "idx.i");
  if(file_exists(cumhist_file)) {
    cumH = mmapfile(cumhist_file, &nH);
    nH /= sizeof(long);
    fprintf(stderr, "reloading cumhist %s\n", cumhist_file);
    fflush(stderr);
  }
  
  else {
    int *H = hist(landmarks, nlandmarks, &nH);
    fprintf(stderr, "hist completed\n");
    fflush(stderr);
    output_ints(H, nH, filename(filename_buf, postings, "hist.i"));

    long *cumH = cumhist(H, nH);
    fprintf(stderr, "cumhist completed\n");
    fflush(stderr);

    output_longs(cumH, nH, filename(filename_buf, postings, "idx.i"));
  }

  long *ptr = (long *)malloc(sizeof(long) * (1+nH));
  if(!ptr) fatal("malloc failed");
  *ptr = 0;
  memcpy(ptr+1, cumH, sizeof(long) * nH);

  long Ndocs = nlandmarks/number_of_landmarks;
  int *result = (int *)malloc(sizeof(int) * nlandmarks);
  if(!result) fatal("malloc failed");
  int *result_end = result + nlandmarks;
  memset(result, -1, sizeof(int) * nlandmarks);

  fprintf(stderr, "Ndocs: %ld\n", Ndocs);
  fprintf(stderr, "number_of_landmarks: %d\n", number_of_landmarks);
  fprintf(stderr, "nlandmarks: %ld\n", nlandmarks);
  fprintf(stderr, "cumH[nH-1] = %ld, nH=%ld\n", cumH[nH-1], nH);
  fflush(stderr);

  if(cumH[nH-1] > nlandmarks) {
    fprintf(stderr, "expected cumH[nH-1] == nlandmarks\n");
    fatal("assertion failed");
  }

  long doc;
  if(docs_end < 0 || docs_end > Ndocs)
    docs_end = Ndocs;
  for(doc=docs_start; doc< docs_end; doc++) {
    // fprintf(stderr, "doc: %d\n", doc);
    for(j=0;j<number_of_landmarks;j++) {
      long offset = doc*number_of_landmarks+j;
      if(offset >= nlandmarks) {
	fprintf(stderr, "offset is too large: offset = %ld, doc = %ld, j = %d, nlandmarks = %ld\n", offset, doc, j, nlandmarks);
	fatal("assertion failed");
      }

      int landmark = landmarks[offset];
      
      if(landmark >= nH || landmark < 0) {
	fprintf(stderr, "landmark is out of range; landmark = %d, nH = %ld\n", landmark, nH);
	fatal("assertion failed");
      }
      long p = ptr[landmark];

      if(p < 0 || p >= nlandmarks) {
	fprintf(stderr, "p is out of range: %ld\n", p);
	fatal("assertion failed");
      }


      if(tick > 0 && (doc % tick == 0))
	fprintf(stderr, "doc: %ld\tlandmark: %d\tp: %ld\tresult[p] = %d\n", doc, landmark, p, result[p]);

      // if(doc >= 21474835) fflush(stderr);
      
      if(result[p] != -1) {
	fprintf(stderr, "result[%ld] is not empty; doc = %ld, j=%d, result[p] = %d\n", p, doc, j, result[p]);
	fatal("assertion failed");
      }

      result[p] = doc;
      ptr[landmark] = ptr[landmark] + 1;
    }
  }

  
  fprintf(stderr, "about to output results\n");
  fflush(stderr);
  output_ints(result, nlandmarks, filename(filename_buf, postings, "i"));
  fprintf(stderr, "done\n");
  fflush(stderr);

  return 0;

}
