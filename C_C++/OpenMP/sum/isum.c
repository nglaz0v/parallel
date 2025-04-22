#include <stddef.h>  // for size_t

float sum(const float *a, size_t n)
{
    float total = 0.;
    #pragma omp parallel for reduction(+:total)
    for (size_t i = 0; i < n; i++) {
        total += a[i];
    }
    return total;
}
