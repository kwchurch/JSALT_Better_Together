#include <stdio.h>
#include <strings.h>
#include "util.h"

void usage()
{
  fatal("venn files");
}

int done(char **inputs, char **ends, int n)
{
  int i;
  for(i=0;i<n;i++)
    if(inputs[i] < ends[i])
      return 0;
  return 1;
}

void my_output(char *s, char *end)
{
  // fprintf(stderr, "# calling my_output\n");
  if(s >= end) printf("***NULL***");
  else for(;s < end && *s != '\n';s++) putchar(*s);
  // fprintf(stderr, "# leaving my_output\n");
}

int my_strcmp(char *a, char *b, char *end_a, char *end_b)
{
  if(a == b) return 0;
  if(a == NULL) return 1;
  if(b == NULL) return -1;
  for(;;a++,b++) {
    if(a >= end_a && b >= end_b) return 0;
    if(a >= end_a) return -1;
    if(b >= end_b) return 1;
    if(*a < *b) return -1;
    if(*a > *b) return 1;
    if(*a == '\n') return 0;
  }
}

int best(char **inputs, char **ends, int n)
{
  // fprintf(stderr, "# calling best\n");
  int i, result = -1;
  for(i=0;i<n;i++)
    if(inputs[i] >= ends[i]) continue;
    else if(result < 0 || my_strcmp(inputs[result], inputs[i], ends[result], ends[i]) > 0)
      result = i;
  // fprintf(stderr, "# leaving best; result = %d\n", result);
  return result;
}

int my_strlen(char *start, char *end)
{
  char *s = start;
  for( ; ; s++)
    if(s >= end || *s == '\n')
      return s-start;
}

void my_advance(int nxt, char **inputs, char **ends, int ninputs)
{
  int i;
  for(i=0;i<ninputs;i++)
    if(i != nxt && inputs[i] < ends[i] && my_strcmp(inputs[i], inputs[nxt], ends[i], ends[nxt]) == 0)
      inputs[i] += my_strlen(inputs[i], ends[i]) + 1;
  i=nxt;
  inputs[i] += my_strlen(inputs[i], ends[i]) + 1;
}

int main(int ac, char **av)
{
  int i, ninputs = ac-1;
  // fprintf(stderr, "# venn: ninputs = %d\n", ninputs);

  long *Ns = (long *)malloc(sizeof(long) * ninputs);
  char **inputs = (char **)malloc(sizeof(char *) * ninputs);
  char **ends = (char **)malloc(sizeof(char *) * ninputs);
  if(!Ns || !inputs || !ends) fatal("malloc failed");

  for(i=0;i<ninputs;i++) { 
    inputs[i] = (char *)mmapfile(av[i+1], Ns+i);
    ends[i] = inputs[i] + Ns[i];
    printf("# %d %s\n", i, av[i+1]);
    // fprintf(stderr, "# found %ld bytes in %s\n", Ns[i], av[i+1]);
  }

  for(;;) {
    int nxt = best(inputs,ends,ninputs);
    if(nxt < 0) break;
    my_output(inputs[nxt], ends[nxt]);
    putchar('\t');
    for(i=0;i<ninputs;i++) {
      if(my_strcmp(inputs[nxt], inputs[i], ends[nxt], ends[i]) == 0) {
	putchar('1');
      }
      else putchar('0');
    }
    putchar('\n');
    my_advance(nxt, inputs, ends, ninputs);
  }

  exit(0);
 }



      
    
  
