#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <strings.h>

FILE *my_fopen(char *fn, char *mode);
void fatal(char *msg);
long fd_length(FILE *fd);
void *mmapfd(FILE *fd, long *n);
void *mmapfile(char *filename, long *n);
void *readcharsfd(FILE *fd, long *n);
void *readchars(char *filename, long *n);
char *filename(char *result, char *prefix, char *suffix);
char *filename2(char *result, char *prefix, char *suffix, int piece);
int file_exists(char *fn);

struct bigram {
  float val;
  int elts[2];
};

struct lbigram {
  float val;
  long elts[2];
};


int bigram_compare(struct bigram *a, struct bigram *b);
int lbigram_compare(struct lbigram *a, struct lbigram *b);

#define TABLE_SIZE 999983

#define MAX_BUF 1024



