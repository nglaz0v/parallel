#include <stdio.h>
#include <stdlib.h>

float sum(const float *, size_t);

#define N 1000000  // we'll sum this many numbers

int main()
{
    float *a = malloc(N * sizeof(float));
    if (a == NULL) {
        perror("malloc");
        return 1;
    }

    // fill the array a
    for (size_t i = 0; i < N; i++) {
        a[i] = .000001;
    }

    printf("%f\n", sum(a, N));
    return 0;
}
