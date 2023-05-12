#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>
#include <search.h>

void usage()
{
  fatal("usage: find_lines [--multiple_matches] [--header] --input lines --fields xxx < keys, where each line starts with key (will create index if necessary in lines.L)\n");
}

// C version of /work/k.church/semantic_scholar/papers/find_lines.py
// if we seek to <offset>, we should see a line that starts with <key>

char *file = NULL;
long nfile = -1;

struct idx {
  long key;			/* each line in file starts with these (numeric) keys */
  long offset; 			/* offsets into files */
};

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

int idx_compare(struct idx *a, struct idx *b)
{
  long na = nfile - a->key;
  long nb = nfile - b->key;
  long n = (na < nb) ? na : nb;
  return strncmp(file + a->key, file + b->key, n);
}

void create_idx(char *outfile, char *infile)
{

  fprintf(stderr, "create_idx: infile = %s, outfile = %s\n", infile, outfile);

  FILE *outfd = fopen(outfile, "wb");
  if(!outfd) fatal("create_idx: open failed");

  long ntext;
  char *text = (char *)mmapfile(infile, &ntext);
  long i, nidx = 0;
  for(i=0;i<ntext;i++)
    if(text[i] == '\n') nidx++;
  fprintf(stderr, "nidx = %ld\n", nidx);
  struct idx *idx = (struct idx *)malloc(sizeof(struct idx) * nidx);
  if(!idx) fatal("malloc failed");
  struct idx *start = idx;

  for(i=0;i<ntext;i++)
    if(text[i] == '\n') {
      i++;
      start->key = atol(text+i);
      start->offset = i;
      start++;
    }
  
  qsort(idx, nidx, sizeof(struct idx), (__compar_fn_t)idx_compare);
  if(fwrite(idx, sizeof(struct idx), nidx, outfd) != nidx)
    fatal("write failed");
  fclose(outfd);
}



void putline(char *line, char *end)
{
  for( ; line < end; line++) {
    if(*line == '\n') break;
    putchar(*line);
  }
  putchar('\n');
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

char *lookup(char *buf,char *piece, char *file, long nfile, struct idx *idx, long nidx)
{
  struct idx query;
  
  // fprintf(stderr, "lookup(piece: %s)\n", piece);

  struct idx *found = NULL;
  if(sscanf(piece, "%ld", &query.key) == 1)
    found = bsearch(&query, idx, nidx, sizeof(struct idx), (__compar_fn_t)idx_compare);
  if(!found) {
    // fprintf(stderr, "lookup: not found, query.key = %ld\n", query.key);
    sprintf(buf, "%ld\tNA:%ld", query.key, query.key);
  }
  else my_strcpy(buf, file + found->offset, file + nfile);
  
  // fprintf(stderr, "found->offset = %ld, nfile = %ld\n", found->offset, nfile);
  return trim(buf);
}
  
int main(int ac, char **av)
{
  char buf[1024];
  int i;
  char *filename = NULL;
  char *fields = NULL;
  int header=0, multiple_matches=0;
  
  for(i=1; i<ac; i++)
    if(strcmp(av[i], "--input") == 0) filename=av[++i];
    else if(strcmp(av[i], "--fields") == 0) fields=av[++i];
    else if(strcmp(av[i], "--header") == 0) header++;
    else if(strcmp(av[i], "--multiple_matches") == 0) multiple_matches++;
    else usage();

  long nidx;
  struct idx query;

  if(filename == NULL) {
    fprintf(stderr, "--input arg is required\n");
    usage();
  }

  // fprintf(stderr, "filename: %s\n", filename);

  file = (char *)mmapfile(filename, &nfile);
  char *end = file + nfile;

  // create index if necessary
  char *fn = my_filename(buf, filename, "L");
  if(!file_exists(fn)) create_idx(fn, filename);
  struct idx *idx = (struct idx *)mmapfile(fn, &nidx);
  nidx /= sizeof(struct idx);

  if(header > 0)putline(file, end);

  if(fields == NULL)
    while(scanf("%ld", &query.key) == 1) {
      struct idx *found = bsearch(&query, idx, nidx, sizeof(struct idx), (__compar_fn_t)idx_compare);
      if(multiple_matches == 0) {
      if(found) putline(file + found->offset, end);
      else printf("NA:%ld\n", query.key);
      }
      else if(found) {
	struct idx *idx_end = idx + nidx;
	struct idx *first_found = found;
	struct idx *last_found = found;
	while(first_found > idx && idx_compare(first_found-1, &query) == 0)
	  first_found--;
	while(last_found+1 < idx_end && idx_compare(last_found+1, &query) == 0)
	  last_found++;
	for(found=first_found;found<=last_found;found++)
	  putline(file + found->offset, end);
      }
    }
  else {
    char lookup_buf[1024];
    for(;;) {
      int npline, i;
      char *pieces[50];
      char *line = fgets(buf, 1024, stdin);
      if(!line) break;
      line[strlen(line)-1]=0;	/* rstrip() */
      char **pline = parse_line(pieces, line, &npline);
      // fprintf(stderr, "parse_line found %d pieces\n", npline);
      for(i=0;i<npline;i++) {
	char *p = pieces[i];
	if(fields[i] == 'L') p = lookup(lookup_buf, p, file, nfile, idx, nidx);
	if(i > 0) putchar('\t');
	printf("%s", p);
      }
      putchar('\n');
    }
  }
}
      
  
