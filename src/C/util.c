#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <strings.h>
#include "util.h"

void fatal(char *msg)
{
  fprintf(stderr, "fatal: %s\n", msg);
  exit(2);
}

FILE *my_fopen(char *fn, char *mode)
{
  FILE *res = fopen(fn, mode);
  if(!res) {
    fprintf(stderr, "my_fopen: %s, mode: %s\n", fn, mode);
    fatal("open failed");
  }
  return res;
}

long fd_length(FILE *fd)
{
  struct stat buf;
  long s = fstat(fileno(fd), &buf);
  return buf.st_size;
}

int file_exists(char *fn)
{
  struct stat buf;
  return stat(fn, &buf) == 0;
}

void *mmapfd(FILE *fd, long *n)
{
  *n = fd_length(fd);
  void *result = mmap(0, *n, PROT_READ, MAP_PRIVATE, fileno(fd), 0);
  if(result == MAP_FAILED) return NULL;
  return result;
}

void *mmapfile(char *filename, long *n)
{
  FILE *fd = fopen(filename, "r");
  if(!fd) {
    fprintf(stderr, "filename = %s\n", filename);
    fatal("mmapfile: open failed");
  }
  void *result = mmapfd(fd, n);
  fclose(fd);
  return result;
}

void *readcharsfd(FILE *fd, long *n)
{
  *n = fd_length(fd);
  void *result = malloc(*n);
  if(!result) fatal("readcharsfd: malloc failed");
  if(fread(result, 1, *n, fd) != *n) fatal("readcharsfd: fread failed");
  return result;
}

void *readchars(char *filename, long *n)
{
  FILE *fd = fopen(filename, "r");
  if(!fd) fatal("readchars: open failed");
  void *result = readcharsfd(fd, n);
  fclose(fd);
  return result;
}

char *filename(char *result, char *prefix, char *suffix)
{
  sprintf(result, "%s.%s", prefix, suffix);
  return result;
}

char *filename2(char *result, char *prefix, char *suffix, int piece)
{
  sprintf(result, "%s.%03d.%s", prefix, piece, suffix);
  return result;
}

int bigram_compare(struct bigram *a, struct bigram *b)
{
  if(a->elts[0] < b->elts[0]) return -1;
  if(a->elts[0] > b->elts[0]) return 1;
  if(a->elts[1] < b->elts[1]) return -1;
  if(a->elts[1] > b->elts[1]) return 1;
  return 0;
}

int lbigram_compare(struct lbigram *a, struct lbigram *b)
{
  if(a->elts[0] < b->elts[0]) return -1;
  if(a->elts[0] > b->elts[0]) return 1;
  if(a->elts[1] < b->elts[1]) return -1;
  if(a->elts[1] > b->elts[1]) return 1;
  return 0;
}

