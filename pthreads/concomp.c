// gcc concomp.c -pthread -o concomp

// https://rosettacode.org/wiki/Concurrent_computing#C

/* Display the strings "Enjoy" "Rosetta" "Code", one string per line, in
 * random order.
 * 
 * Note: since threads are created one after another, it is likely that
 * the execution of their code follows the order of creation. To make
 * this less evident, I've added the bang idea using condition: the
 * thread really executes their code once the gun bang is heard.
 * Nonetheless, I still obtain the same order of creation (Enjoy,
 * Rosetta, Code), and maybe it is because of the order locks are
 * acquired. The only way to obtain randomness seems to be to add random
 * wait in each thread (or wait for special cpu load condition)
 */

#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

pthread_mutex_t condm = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int bang = 0;

#define WAITBANG() do { \
   pthread_mutex_lock(&condm); \
   while( bang == 0 ) \
   { \
      pthread_cond_wait(&cond, &condm); \
   } \
   pthread_mutex_unlock(&condm); } while(0);\

void *t_enjoy(void *p)
{
  WAITBANG();
  printf("Enjoy\n");
  pthread_exit(0);
}

void *t_rosetta(void *p)
{
  WAITBANG();
  printf("Rosetta\n");
  pthread_exit(0);
}

void *t_code(void *p)
{
  WAITBANG();
  printf("Code\n");
  pthread_exit(0);
}

typedef void *(*threadfunc)(void *);
int main()
{
   int i;
   pthread_t a[3];
   threadfunc p[3] = {t_enjoy, t_rosetta, t_code};
   
   for(i=0;i<3;i++)
   {
     pthread_create(&a[i], NULL, p[i], NULL);
   }
   sleep(1);
   bang = 1;
   pthread_cond_broadcast(&cond);
   for(i=0;i<3;i++)
   {
     pthread_join(a[i], NULL);
   }
}
