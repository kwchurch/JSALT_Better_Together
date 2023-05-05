#include <stdio.h>
#include <strings.h>
#include "util.h"

void usage()
{
  fatal("uniq_bigrams < bigrams > bigrams.uniq");
}

void my_output(struct bigram *out)
{
  if(out->val != 0) {
    if(fwrite(out, sizeof(struct bigram), 1, stdout) != 1)
      fatal("write failed");
  }
 }

int main(int ac, char **av)
{

  if(ac != 1) usage();
  struct bigram b;
  struct bigram out;
  out.val=0;

  while(fread(&b, sizeof(struct bigram), 1, stdin) == 1) {
    if(bigram_compare(&out, &b) == 0)
      out.val += b.val;
    else {
      my_output(&out);
      memcpy(&out, &b, sizeof(struct bigram));
    }
  }

  my_output(&out);
 }

