// gcc atomupd.c -fopenmp -o atomupd

// https://rosettacode.org/wiki/Atomic_updates#With_OpenMP

/* Define a data type consisting of a fixed number of 'buckets', each
 * containing a nonnegative integer value, which supports operations to:
 * - get the current value of any bucket
 * - remove a specified amount from one specified bucket and add it to
 *   another, preserving the total of all bucket values, and clamping
 *   the transferred amount to ensure the values remain non-negative
 * In order to exercise this data type, create one set of buckets, and
 * start three concurrent tasks:
 * - As often as possible, pick two buckets and make their values closer
 *   to equal.
 * - As often as possible, pick two buckets and arbitrarily redistribute
 *   their values.
 * - At whatever rate is convenient, display (by any means) the total
 *   value and, optionally, the individual values of each bucket.
 * The display task need not be explicit; use of e.g. a debugger or
 * trace tool is acceptable provided it is simple to set up to provide
 * the display.
 * This task is intended as an exercise in atomic operations. The sum of
 * the bucket values must be preserved even if the two tasks attempt to
 * perform transfers simultaneously, and a straightforward solution is
 * to ensure that at any time, only one transfer is actually occurring —
 * that the transfer operation is atomic.
 */

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define irand(n) (n * (double)rand()/(RAND_MAX + 1.0))

int bucket[10];
int main()
{
	int i;
	for (i = 0; i < 10; i++) bucket[i] = 1000;
	omp_set_num_threads(3);

	#pragma omp parallel private(i)
	for (i = 0; i < 10000; i++) {
		int from, to, mode, diff = 0, sum;

		from = irand(10);
		do { to = irand(10); } while (from == to);
		mode = irand(10);

		switch (mode) {
		case 0:
		case 1:
		case 2:	/* equalize */
			diff = (bucket[from] - bucket[to]) / 2;
			break;

		case 3: /* report */
			sum = 0;
			for (int j = 0; j < 10; j++) {
				printf("%d ", bucket[j]);
				sum += bucket[j];
			}
			printf(" Sum: %d\n", sum);
			continue;

		default: /* random transfer */
			diff = irand(bucket[from]);
			break;
		}

		#pragma omp critical
		{
			bucket[from] -= diff;
			bucket[to]   += diff;
		}
	}

	return 0;
}
