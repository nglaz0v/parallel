// g++ -fopenmp speedup.cpp -o speedup

#include <iostream>
#include <vector>
#include <ctime>
#include <chrono>
#include <omp.h>

int main() {
    const int num_elements = 100000000;

    std::vector<double> a(num_elements, 1.0);
    std::vector<double> b(num_elements, 2.0);
    std::vector<double> c(num_elements, 0.0);

    // Serial version
    auto start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num_elements; i++) {
        c[i] = a[i] * b[i];
    }
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration_serial = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    // Parallel version with OpenMP
    start_time = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for
    for (int i = 0; i < num_elements; i++) {
        c[i] = a[i] * b[i];
    }
    end_time = std::chrono::high_resolution_clock::now();
    auto duration_parallel = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Serial execution time: " << duration_serial << " ms" << std::endl;
    std::cout << "Parallel execution time: " << duration_parallel << " ms" << std::endl;
    std::cout << "Speedup: " << static_cast<double>(duration_serial) / duration_parallel << std::endl;

    return 0;
}
