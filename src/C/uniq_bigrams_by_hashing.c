#include <stdio.h>
#include <strings.h>
#include "util.h"

struct bigram table[TABLE_SIZE];

long hash(struct bigram *b, long N)
{
  long h = (b->elts[0] * N + b->elts[1]) % TABLE_SIZE;
  if(h < 0) h += TABLE_SIZE;
  return h;
}

void my_output(struct bigram *out)
{
  if(out->val != 0) {
    if(fwrite(out, sizeof(struct bigram), 1, stdout) != 1)
      fatal("write failed");
  }
}

void output_table()
{
  struct bigram *t = table;
  struct bigram *end = t + TABLE_SIZE;
  for( ; t<end; t++) {
    my_output(t);
  }
 }

int empty(struct bigram *cell)
{
  return (cell->elts[0] == 0) && (cell->elts[1] == 0);
}

int main(int ac, char **av)
{
  struct bigram b;
  struct bigram out;
  long N = 300000000;

  memset(table, 0, sizeof(struct bigram) * TABLE_SIZE);
  
  while(fread(&b, sizeof(struct bigram), 1, stdin) == 1) {
    int h = hash(&b, N);
    if(h < 0 || h >= TABLE_SIZE) fatal("confusion");

    struct bigram *cell = table+h;
    if(empty(cell)) memcpy(cell, &b, sizeof(struct bigram));
    else if (bigram_compare(cell, &b) == 0) cell->val += b.val;
    else {
      my_output(cell);
      memcpy(cell, &b, sizeof(struct bigram));
    }
  }
  
  output_table();
 }

