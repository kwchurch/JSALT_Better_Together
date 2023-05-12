#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>
#include <search.h>

int verbose = 0;
int field = 0;
int delimiter = '\n';
int multiple_matches = 0;
int partial_matches = 0;
int check_order = 0;
int sort_index = 0;

// This would be a nice feature to implement
int prefix_matches_ok = 0;

void usage()
{
  fatal("usage: find_in_sorted_lines [--sort_index] [--check_order] [--multiple_matches] [--partial_matches] --delimiter <delimiter> --field <field> --input lines < keys, where each line starts with key (assumes lines are sorted)\n");
}

// Assume lines is a sorted text file 

char *query = NULL;
char *file = NULL;
long nfile = -1;

long *offsets = NULL;
long noffsets = -1;

void putline(FILE *fd, char *line, char *end)
{
  for( ; line != end; line++) {
    if(*line == '\n' || *line == 0) break;
    fputc(*line, fd);
  }
  fputc('\n', fd);
}

void my_strcpy(char *buf, char *line, char *end)
{
  int i;
  for(i=0 ; line < end; line++,i++) {
    if(*line == '\n') break;
    buf[i] = *line;
  }
  buf[i] = 0;
}

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

int my_eos(char x)
{
  return x == 0 || x == '\n' || x == '\t';
}

char *my_trim(char *x, int f)
{
  if(f <= 1) return x;
  for(;;x++) {
    if(*x == delimiter)
      return my_trim(x+1, f-1);
    if(*x == '\n')
      return "";
  }
  return "";
}

int my_strcmp(char *a, char *b)
{
  a = my_trim(a, field);
  b = my_trim(b, field);

  for(;;a++,b++) {
    int a_eos = my_eos(*a);
    int b_eos = my_eos(*b);

    if(a_eos && b_eos) return 0;
    if(partial_matches && (a_eos || b_eos)) return 0;

    if(a_eos) return 1;
    if(b_eos) return -1;
    if(*a < *b) return -1;
    if(*a > *b) return 1;
  }
}  

int my_compare(long *a, long *b)
{
  char *aa, *bb;

  if(a > offsets && a < offsets + noffsets)
    aa = file + *a;
  else aa = query;

  if(b > offsets && b < offsets + noffsets)
    bb = file + *b;
  else bb = query;


  int comp = my_strcmp(aa, bb);
  if(verbose) {
    putline(stderr, aa, file + nfile);
    putline(stderr, bb, file + nfile);
    fprintf(stderr, "my_compare: %d\n\n", comp);
  }

  return comp;
}

void my_output(long offset, FILE *fd)
{
  if(fwrite(&offset, sizeof(long), 1, fd) != 1)
    fatal("write failed");
}

void create_offsets(char *outfile, char *file_contents, long nfile_contents)
{

  fprintf(stderr, "create_offsets: outfile = %s\n", outfile);

  FILE *outfd = fopen(outfile, "wb");
  if(!outfd) fatal("create_offsets: open failed");

  long offset = 0;
  my_output(0, outfd);

  for( ; offset < nfile_contents ;offset++) {
    int c = file_contents[offset];
    if(c == EOF) break;
    if(c == '\n') my_output(offset+1, outfd);
  }

  fclose(outfd);
}

char **parse_line(char **pieces, char *line, int *nfields)
{
  int i;
  int nf = 0;
  pieces[nf++] = line;
  for(i=0; line[i]; i++)
    if(line[i] == '\t') {
      line[i++] = 0;
      pieces[nf++] = line + i;
    }
  *nfields = nf;
  return pieces;
}

char *trim(char *s)
{
  for(; ;s++) {
    if(*s == 0) return s;
    if(*s == '\t') return s+1;
  }
}

long *my_find(char *query, long *offsets, long noffsets)
{
  long *lo = offsets;
  long *hi = offsets + noffsets;
  int len = strlen(query);
  while (hi - lo > 5) {
    long *mid = lo + (hi - lo)/2;
    int comp = strncmp(query, file + *mid, len);
    if(comp == 0) return mid;
    if(comp > 0) lo = mid;
    else hi = mid;
  }
  for( ; lo <  hi; lo++)
    if(strncmp(query, file + *lo, len) == 0) return lo;
  return NULL;
}


/* char *lookup(char *buf,char *piece, char *file, long nfile, struct idx *idx, long nidx) */
/* { */
  
  
/*   if(sscanf(piece, "%ld", &query.key) != 1) fatal("confusion in lookup"); */
/*   struct idx *found = bsearch(&query, idx, nidx, sizeof(struct idx), (__compar_fn_t)idx_compare); */
/*   if(!found) { */
/*     // fprintf(stderr, "lookup: not found, query.key = %ld\n", query.key); */
/*     sprintf(buf, "%ld\tNA:%ld\n", query.key, query.key); */
/*   } */
/*   else my_strcpy(buf, file + found->offset, file + nfile); */
  
/*   // fprintf(stderr, "found->offset = %ld, nfile = %ld\n", found->offset, nfile); */
/*   return trim(buf); */
/* } */
  
int main(int ac, char **av)
{
  char buf[1024];
  int i;
  char *filename = NULL;
  char *fields = NULL;
  
  for(i=1; i<ac; i++)
    if(strcmp(av[i], "--input") == 0) filename=av[++i];
    else if(strcmp(av[i], "--field") == 0) field=atoi(av[++i]);
    else if(strcmp(av[i], "--delimiter") == 0) delimiter=av[++i][0];
    else if(strcmp(av[i], "--multiple_matches") == 0) multiple_matches++;
    else if(strcmp(av[i], "--partial_matches") == 0) partial_matches++;
    else if(strcmp(av[i], "--check_order") == 0) check_order++;
    else if(strcmp(av[i], "--sort_index") == 0) sort_index++;
    else if(strcmp(av[i], "--verbose") == 0) verbose++;
  // else if(strcmp(av[i], "--fields") == 0) fields=av[++i];
    else usage();

  if(filename == NULL) {
    fprintf(stderr, "--input arg is required\n");
    usage();
  }

  // fprintf(stderr, "filename: %s\n", filename);

  file = (char *)mmapfile(filename, &nfile);
  char *end = file + nfile;


  // create index if necessary
  char *fn = my_filename(buf, filename, "L");
  if(!file_exists(fn)) create_offsets(fn, file, nfile);
  offsets  = (long *)mmapfile(fn, &noffsets);
  noffsets /= sizeof(long);

  query = buf;

  if(sort_index != 0) {
    fprintf(stderr, "sorting indexes ...");
    long *new_offsets = (long *)malloc(noffsets * sizeof(long));
    if(!new_offsets) fatal("malloc failed");
    memcpy(new_offsets, offsets, noffsets * sizeof(long));
    
    qsort(new_offsets, noffsets, sizeof(long), (__compar_fn_t)my_compare);
    char *fn = my_filename(buf, filename, "L");
    FILE *fd = fopen(fn, "wb");
    if(fwrite(new_offsets, sizeof(long), noffsets, fd) != noffsets)
      fatal("write failed");
    fclose(fd);
    offsets = new_offsets;
    fprintf(stderr, "done.\n");
  }

  if(check_order != 0) {
    long o;
    long cnt[3];
    memset(cnt, 0, 3*sizeof(long));
    printf("noffsets = %ld\n", noffsets);
    for(o=1;o<noffsets;o++) {
      int comp = my_compare(offsets+o-1,offsets+o);
      if(comp < 0) cnt[0]++;
      if(comp == 0) cnt[1]++;
      if(comp > 0) cnt[2]++;
      if(o%100000 == 0) {
	fprintf(stderr, "\no = %9ld, comps = %ld, %ld, %ld\n", o, cnt[0],cnt[1],cnt[2]);
	fprintf(stderr, "comp = %d, o = %ld, offsets[o-1] = %ld, offsets[o] = %ld, field = %d, delimiter = %c\n", comp, o, offsets[o-1], offsets[o], field, delimiter);
	putline(stderr, file + offsets[o-1], file + nfile);
	putline(stderr, file + offsets[o], file + nfile);
	fprintf(stderr, "trims:\n");
	putline(stderr, my_trim(file + offsets[o-1], field), file + nfile);
	putline(stderr, my_trim(file + offsets[o], field), file + nfile);
      }
    }
    
    fprintf(stderr, "comps = %ld, %ld, %ld\n", cnt[0],cnt[1],cnt[2]);
    

	/* fatal("check_order failed"); */

  }


  while(fgets(buf, 1024, stdin) != NULL) {
    int l = strlen(buf);
    if(buf[l-1] == '\n')
      buf[l-1] = 0;
    query = buf;
    long *found = my_find(query, offsets, noffsets);
    if(found) {
      // fprintf(stderr, "found = %ld, offsets[0] = %ld, offsets[%ld] = %ld\n", found, offsets[0], noffsets-1, offsets[noffsets-1]);
      if(!multiple_matches)
	putline(stdout, file + *found, end);
    }
    // else fprintf(stderr, "found = NA\n");

    if(!found) printf("%s\tNA\n", query);
    else if(multiple_matches) {
      int len = strlen(query);
      while(strncmp(query, file + found[-1], len) == 0) found--;

      /* fprintf(stderr, "\nBEFORE\n"); */
      /* fprintf(stderr, "%s\t", query); */
      /* putline(stderr, file + found[-1], end); */

      for(;strncmp(query, file + *found, len) == 0; found++) {
	printf("%s\t", query);
	putline(stdout, file + *found, end);
      }
      
      /* fprintf(stderr, "\nAFTER\n"); */
      /* fprintf(stderr, "%s\t", query); */
      /* putline(stderr, file + *found, end); */
    }
  }
}
      
  /*     first = last = &found; */
  /*     int len = strlen(query); */
  /*     while(first[0] > 0 && strncmp(query, file + first[-1], len) == 0) first--; */
  /*     while(last[0] < noffsets && strncmp(query, file + last[1], len) == 0) last++; */

  /*     for(m=first;m<=last;m++) { */
  /* 	printf("%s\t", query); */
  /* 	putline(stdout, file + *m, end); */
  /*     } */
  /*   } */
  /*   else putline(stdout, file + *found, end); */
  /* } */

  /* while(fgets(buf, 1024, stdin) != NULL) { */
  /*   int l = strlen(buf); */
  /*   if(buf[l-1] == '\n') */
  /*     buf[l-1] = 0; */
  /*   query = buf; */
  /*   long *found = bsearch(query, offsets, noffsets, sizeof(long), (__compar_fn_t)my_compare); */
  /*   if(found) { */
  /*     fprintf(stderr, "found = %ld, offsets[0] = %ld, offsets[%ld] = %ld\n", found, offsets[0], noffsets-1, offsets[noffsets-1]); */
  /*     putline(stderr, file + *found, end); */
  /*   } */
  /*   else fprintf(stderr, "found = NA\n"); */

  /*   if(!found) printf("%s\tNA\n", query); */
  /*   else if(multiple_matches) { */
  /*     long *m, *first, *last; */
  /*     first = last = found; */
  /*     while(my_compare((long*)query, first-1) == 0 && *first >= 0) first--; */
  /*     fprintf(stderr, "first = %ld\n", first); */
  /*     while(my_compare((long*)query, last+1) == 0 && *last < noffsets) last++; */
  /*     fprintf(stderr, "last = %ld\n", last); */
  /*     for(m=first;m<=last;m++) { */
  /* 	printf("%s\t", query); */
  /* 	putline(stdout, file + *m, end); */
  /*     } */
  /*   } */
  /*   else putline(stdout, file + *found, end); */
  /* } */
