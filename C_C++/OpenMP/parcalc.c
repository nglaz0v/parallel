// gcc prime.c -fopenmp -o prime

// https://rosettacode.org/wiki/Parallel_calculations#C

/* The code finds the largest first prime factor, but does not return
 * the factor list: it's just a matter of repeating the prime factor
 * test, which adds clutter but does not make the code any more
 * interesting. For that matter, the code uses the dumbest prime
 * factoring method, and doesn't even test if the numbers can be divided
 * by 2.
 * */

#include <stdio.h>
#include <omp.h>

int main()
{
    int data[] = {12757923, 12878611, 12878893, 12757923, 15808973, 15780709, 197622519};
    int largest, largest_factor = 0;

    omp_set_num_threads(4);
    /* "omp parallel for" turns the for loop multithreaded by making each thread
     * iterating only a part of the loop variable, in this case i; variables declared
     * as "shared" will be implicitly locked on access
     */
    #pragma omp parallel for shared(largest_factor, largest)
    for (int i = 0; i < 7; i++) {
        int p, n = data[i];

        for (p = 3; p * p <= n && n % p; p += 2);
        if (p * p > n) p = n;
        if (p > largest_factor) {
            largest_factor = p;
            largest = n;
            printf("thread %d: found larger: %d of %d\n",
                    omp_get_thread_num(), p, n);
        } else {
            printf("thread %d: not larger:   %d of %d\n",
                    omp_get_thread_num(), p, n);
        }
    }

    printf("Largest factor: %d of %d\n", largest_factor, largest);
    return 0;
}
