// gcc concomp.c -fopenmp -o concomp

// https://rosettacode.org/wiki/Concurrent_computing#OpenMP

/* Display the strings "Enjoy" "Rosetta" "Code", one string per line, in
 * random order.
 */

#include <stdio.h>
#include <omp.h>

int main()
{
	const char *str[] = { "Enjoy", "Rosetta", "Code" };
	#pragma omp parallel for num_threads(3)
	for (int i = 0; i < 3; i++)
		printf("%s\n", str[i]);
	return 0;
}
