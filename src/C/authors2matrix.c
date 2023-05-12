#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>
#include <search.h>

#define MAXLINE 200000

int long_compare(long *a, long *b)
{
  if(*a < *b) return -1;
  if(*a > *b) return 1;
  return 0;
}

struct node_map{
  int *old_to_new;
  int *new_to_old;
  long nold_to_new, nnew_to_old;
};

struct node_map *the_node_map = NULL;

int NEW_TO_OLD = 1;
int OLD_TO_NEW = 0;

long map_node(long node, int new_to_old)
{
  struct node_map *M = the_node_map;

  if(!M) return node;
  long N;
  int *MM;

  if(new_to_old) {
    MM = M->new_to_old;
    N = M->nnew_to_old;
  }
  else {
    MM = M->old_to_new;
    N = M->nold_to_new;
  }

  if(node < 0 || node >= N) {
    fprintf(stderr, "warning: node = %ld; N = %ld\n", node, N);
    // fatal("confusion in map_node");
    return 0;
  }

  return MM[node];
}

long map_author(long author_id, long *authors, long nauthors)
{
  long *found = bsearch(&author_id, authors, nauthors, sizeof(long), long_compare);
  // long *found = bsearch(&author_id, authors, nauthors, sizeof(long), (__compar_fn_t)long_compare);
  if(found) return found - authors;
  else return -1;
}

char *my_filename(char *result, char *filename, char *suffix)
{
  sprintf(result, "%s.%s", filename, suffix);
  return result;
}

void init_node_map(char *filename)
{
  char buf[MAXLINE];
  the_node_map = (struct node_map *)malloc(sizeof(struct node_map));
  if(!the_node_map) fatal("malloc failed");

  the_node_map->old_to_new = (int *)mmapfile(my_filename(buf, filename, "old_to_new.i"), &the_node_map->nold_to_new);
  the_node_map->new_to_old = (int *)mmapfile(my_filename(buf, filename, "new_to_old.i"), &the_node_map->nnew_to_old);
  the_node_map->nold_to_new /= sizeof(int);
  the_node_map->nnew_to_old /= sizeof(int);
}


char **split(char **pieces, char *line, int *nfields, char *delimiters)
{
  int i;
  int nf = 0;
  pieces[nf++] = line;
  for(i=0; line[i]; i++)
    if(strchr(delimiters, line[i])) {
      line[i++] = 0;
      pieces[nf++] = line + i;
    }
  *nfields = nf;
  return pieces;
}

void usage()
{
  fatal("authors2matrix --slurm --input --output --paper_map --authors");
}

// parser.add_argument('-a', '--authors', help="*.L file", default='/work/k.church/semantic_scholar/authors/authors.id.L')

int main(int ac, char **av)
{
  char buf[MAXLINE];
  // char *pieces[MAXLINE];
  int npieces, i, slurm = -1;
  char *input_filename, *output_filename;
  long nauthors = 0;
  long *authors = NULL;

  for(i=1;i<ac;i++)
    if(strcmp(av[i], "--slurm") == 0) slurm=atoi(av[++i]);
    else if(strcmp(av[i], "--input") == 0) input_filename=av[++i];
    else if(strcmp(av[i], "--output") == 0) output_filename=av[++i];
    else if(strcmp(av[i], "--paper_map") == 0) init_node_map(av[++i]);
    else if(strcmp(av[i], "--authors") == 0) {
      authors = (long *)mmapfile(av[++i], &nauthors);
      nauthors /= sizeof(long);
    }
    else usage();

  // fprintf(stderr, "input_filename = %s\n", input_filename);
  // fprintf(stderr, "output_filename = %s\n", output_filename);

  if(slurm >= 0) {
    sprintf(buf, input_filename, slurm);
    input_filename = strdup(buf);
    sprintf(buf, output_filename, slurm);
    output_filename = strdup(buf);
  }

  // fprintf(stderr, "input_filename = %s\n", input_filename);
  // fprintf(stderr, "output_filename = %s\n", output_filename);

  FILE *input = fopen(input_filename, "r");
  FILE *output = fopen(output_filename, "w");

  if(!input) fatal("open failed: input");
  if(!output) fatal("open failed: output");

  long old_paper_id, old_author_id, citations;

  while(fgets(buf, MAXLINE, input) != NULL) {
    if(sscanf(buf, "%ld\t%ld\t%ld", &old_paper_id, &old_author_id, &citations) == 3) {
      long new_paper_id = map_node(old_paper_id, OLD_TO_NEW);
      long new_author_id = map_author(old_author_id, authors, nauthors);
      if(new_author_id >= 0) fprintf(output, "%ld\t%ld\t%ld\t%ld\t%ld\n", new_paper_id, new_author_id, citations, old_paper_id, old_author_id);
    }
  }

  /* while(fgets(buf, MAXLINE, input) != NULL) { */
  /*   int j; */
  /*   if(strlen(buf) >= MAXLINE) fatal("input line is too long"); */
  /*   // fprintf(stderr, "input line: %s", buf); */
  /*   split(pieces, buf, &npieces, "\t|"); */
  /*   // if(npieces < 2) continue; */
  /*   // fprintf(stderr, "npieces = %d\n", npieces); */
  /*   long old_paper_id, old_author_id; */
  /*   sscanf(pieces[0], "%ld", &old_paper_id); */
  /*   long new_paper_id = map_node(old_paper_id, OLD_TO_NEW); */
  /*   // if(new_paper_id <= 0) continue; */
  /*   for(j=1;j<npieces;j++) { */
  /*     sscanf(pieces[j], "%ld", &old_author_id); */
  /*     long new_author_id = map_author(old_author_id, authors, nauthors); */
  /*     if(new_author_id >= 0) fprintf(output, "%ld\t%ld\t%ld\t%ld\n", new_paper_id, new_author_id, old_paper_id, old_author_id); */
  /*   } */
  /* } */

  exit(0);
}
