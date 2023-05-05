#include <stdio.h>
#include "util.h"
#include <memory.h>
#include <math.h>
#include <errno.h>
#include <strings.h>
#include <stdlib.h>

void usage()
{
  fatal("usage: BFS /work/k.church/semantic_scholar/citations/graphs/citations.G [-max_depth <n>] [-max_queue <n>] -print_steps -no_destination > report");
}

char *fname(char *buf, char *prefix, char *suffix)
{
  sprintf(buf, "%s.%s", prefix, suffix);
  return buf;
}

long *malloc_longs(long n)
{
  fprintf(stderr, "malloc_longs: n = %ld\n", n);
  long *res = (long *)malloc(n * sizeof(long));
  if(!res) fatal("malloc_ints: failed");
  // should not be necessary
  memset(res, 0, n * sizeof(long));
  fprintf(stderr, "malloc_longs: done\n", n);
  return res;
}

int *malloc_ints(long n)
{
  fprintf(stderr, "n = %ld\n", n);
  int *res = (int *)malloc(n * sizeof(int));
  if(!res) fatal("malloc_ints: failed");
  // should not be necessary
  memset(res, 0, n * sizeof(int));
  return res;
}

long *cumsum(long *X, long N)
{
  fprintf(stderr, "calling cumsum: N = %ld\n", N);

  long i;
  long *res = malloc_longs(N+1);
  if(!res) fatal("malloc failed");
  res[0] = 0;
  for(i = 0; i<N; i++)
    res[i+1] = res[i] + X[i];
  return res;
}

long *index_ints(int *X, long N, long *nresult)
{
  fprintf(stderr, "calling index_ints\n");
  long i, n = X[N-1]+1;
  *nresult = n+1;
  long *res = (long *)malloc(sizeof(long) * n);
  if(!res) fatal("malloc failed");
  memset(res, 0, sizeof(long)*n);
  for(i=0;i<N;i++)
    res[X[i]]++;
  return cumsum(res, N);
}

long *memoize_index(char *filename, int *X, long N)
{
  // fprintf(stderr, "calling memoize_index: %s\n", filename);
  char buf[1024];
  sprintf(buf, "%s.idx", filename);
  FILE *fd = fopen(buf, "rb");
  long nres;
  if(!fd) {
    FILE *fd = fopen(buf, "wb");
    long *res = index_ints(X, N, &nres);
    fprintf(stderr, "index_size = %ld\n", nres);
    if(fwrite(res, sizeof(long), nres, fd) != nres)
      fatal("write failed");
    fclose(fd);
    return res;
  }

  return (long *)mmapfile(buf, &nres);
}


/* int *cumsum(int *X, long N) */
/* { */
/*   fprintf(stderr, "calling cumsum: N = %ld\n", N); */

/*   int i; */
/*   int *res = malloc_ints(N+1); */
/*   res[0] = 0; */
/*   for(i = 0; i<N; i++) */
/*     res[i+1] = res[i] + X[i]; */
/*   return res; */
/* } */

/* int *index_ints(int *X, long N, long *nresult) */
/* { */
/*   fprintf(stderr, "calling index_ints: N = %ld\n", N); */
/*   long i, n = X[N-1]+1; */
/*   *nresult = n+1; */
/*   int *res = (int *)malloc(sizeof(int) * n); */
/*   if(!res) fatal("malloc failed"); */
/*   memset(res, 0, sizeof(int)*n); */
/*   for(i=0;i<N;i++) */
/*     res[X[i]]++; */
/*   return cumsum(res, N); */
/* } */

/* int *memoize_index(char *filename, int *X, long N) */
/* { */
/*   fprintf(stderr, "calling memoize_index: %s\n", filename); */
/*   char buf[1024]; */
/*   sprintf(buf, "%s.idx", filename); */
/*   FILE *fd = fopen(buf, "rb"); */
/*   long nres; */
/*   if(!fd) { */
/*     FILE *fd = fopen(buf, "wb"); */
/*     int *res = index_ints(X, N, &nres); */
/*     fprintf(stderr, "index_size = %ld\n", nres); */
/*     if(fwrite(res, sizeof(int), nres, fd) != nres) */
/*       fatal("write failed"); */
/*     fclose(fd); */
/*     return res; */
/*   } */

/*   return (int *)mmapfile(buf, &nres); */
/* } */


int max_depth = -1;
long max_queue = 100000000;

struct pair {
  int node, dist;
};

struct pair *queue=NULL;
struct pair *head=NULL;
struct pair *tail=NULL;
char *visited;
long *Xidx;
int *X, *Y;
long nXidx = 0;
long nX = 0;
long nY = 0;

// return -1 on failure
int my_push(int dist, int *nodes, int n)
{
  // fprintf(stderr, "my_push: dist = %d, int %d\n", dist, n);
  if(!tail) fatal("queue was not initialized");
  // if(tail+n >= queue + max_queue) return -1;

  struct pair *qend = queue + max_queue;
  int *end = nodes + n;
  for( ; nodes < end; nodes++)
    if(visited[*nodes] == 0) {
      visited[*nodes] = 1;
      tail->node = *nodes;
      tail->dist = dist;
      if(tail++ > qend) return -1;
    }
  return 0;
}

void do_print_steps(int x, int dist, int *nodes, int n)
{
  if(!tail) fatal("queue was not initialized");
  if(tail+n >= queue + max_queue)
    return;

  int *end = nodes + n;
  for( ; nodes < end; nodes++)
    if(visited[*nodes] == 0)
      printf("steps\t%d\t%d\t%d\n", dist, x, *nodes);
}

struct pair *my_pop()
{
  if(!head) fatal("queue was not initialized");
  if(head >= tail) fatal("queue underflow");
  return head++;
}

int max_depth_exceeded = -3;
int queue_exhausted = -2;

int path(int x, int y, long *steps, int print_steps)
{
  head=queue;
  tail=queue+1;
  *steps = 0;
  if(x == y) return 0;
  memset(visited, 0, nXidx);
  head->dist = 0;
  head->node = x;
  while(head < tail) {
    *steps = tail - queue;
    long low;
    struct pair *p = my_pop();

    if(p->node == y) return p->dist;
    // if(visited[p->node]) continue;
    if(p->node >= nXidx) continue;
    if(p->node < 0) continue;
    if(p->node == 0) low = 0;
    else low = Xidx[p->node];   // used to be: low = Xidx[p->node -1];
    // if(print_steps) do_print_steps(x, p->dist + 1, Y+low, Xidx[p->node + 0] - low);   used to be + 0; now +1
    if(print_steps) do_print_steps(x, p->dist + 1, Y+low, Xidx[p->node + 1] - low);
    if(max_depth >= 0 && p->dist >= max_depth)
      return max_depth_exceeded;
    if(my_push(p->dist + 1, Y+low, Xidx[p->node + 1] - low) < 0) // used to be + 0; now +1
      return queue_exhausted;
  }
  return -1;
}

int main(int ac, char **av)
{
  char buf[MAX_BUF];
  int i, print_steps=0, no_destination=0;
  for(i=2;i<ac;i++) {
    if(strcmp(av[i], "-max_queue") == 0) max_queue = atol(av[++i]);
    else if(strcmp(av[i], "-max_depth") == 0) max_depth = atoi(av[++i]);
    else if(strcmp(av[i], "-print_steps") == 0) print_steps++;
    else if(strcmp(av[i], "-no_destination") == 0) no_destination++;
    else usage();
  }

  queue = (struct pair *)malloc(sizeof(struct pair) * max_queue);
  if(!queue) fatal("malloc failed");
  int x,y;
  long steps;
  X = (int *)mmapfile(fname(buf, av[1], "X.i"), &nX);
  nX /= sizeof(int);
  Xidx = memoize_index(fname(buf, av[1], "X.i"), X, nX);
  // Xidx = (int *)mmapfile(fname(buf, av[1], "X.idx.i"), &nXidx);
  Y = (int *)mmapfile(fname(buf, av[1], "Y.i"), &nY);
  // nXidx /= sizeof(int);
  nXidx = nX + 1;
  nY /= sizeof(int);
  visited = (char *)malloc(nXidx);
  if(!visited) fatal("malloc failed");

  if(no_destination) 
    while(fgets(buf, MAX_BUF, stdin) != NULL && sscanf(buf, "%d", &x) == 1) {
      int d = path(x, -1, &steps, print_steps);
    }
    
  else while(fgets(buf, MAX_BUF, stdin) != NULL && sscanf(buf, "%d%d", &x, &y) == 2) {
      int d = path(x, y, &steps, print_steps);
      printf("%d\t%ld\t%s", d, steps, buf);
      fflush(stdout);
    }
}

