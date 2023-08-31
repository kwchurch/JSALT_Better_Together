#include <stdio.h>
#include <strings.h>
#include "util.h"

struct lbigram table[TABLE_SIZE];

long hash(struct lbigram *b, long N)
{
  long h = (b->elts[0] * N + b->elts[1]) % TABLE_SIZE;
  if(h < 0) h += TABLE_SIZE;
  return h;
}

void my_output(struct lbigram *out)
{
  if(out->val != 0) {
    if(fwrite(out, sizeof(struct lbigram), 1, stdout) != 1)
      fatal("write failed");
  }
}

void output_table()
{
  struct lbigram *t = table;
  struct lbigram *end = t + TABLE_SIZE;
  for( ; t<end; t++) {
    my_output(t);
  }
 }

int empty(struct lbigram *cell)
{
  return (cell->elts[0] == 0) && (cell->elts[1] == 0);
}

int main(int ac, char **av)
{
  struct lbigram b;
  struct lbigram out;
  long N = 300000000;

  memset(table, 0, sizeof(struct lbigram) * TABLE_SIZE);
  
  while(fread(&b, sizeof(struct lbigram), 1, stdin) == 1) {
    int h = hash(&b, N);
    if(h < 0 || h >= TABLE_SIZE) fatal("confusion");

    struct lbigram *cell = table+h;
    if(empty(cell)) memcpy(cell, &b, sizeof(struct lbigram));
    else if (lbigram_compare(cell, &b) == 0) cell->val += b.val;
    else {
      my_output(cell);
      memcpy(cell, &b, sizeof(struct lbigram));
    }
  }
  
  output_table();
 }

