// g++ -fopenmp mandelbrot.cpp -o mandelbrot

#include <iostream>
#include <fstream>
#include <complex>
#include <vector>
#include <omp.h>

const int width = 2000;
const int height = 2000;
const int max_iterations = 1000;

int mandelbrot(const std::complex<double> &c) {
    std::complex<double> z = c;
    int n = 0;
    while (abs(z) <= 2 && n < max_iterations) {
        z = z * z + c;
        n++;
    }
    return n;
}

int main() {
    std::vector<std::vector<int>> values(height, std::vector<int>(width));

    // Calculate the Mandelbrot set using OpenMP
    #pragma omp parallel for schedule(dynamic)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            double real = (x - width / 2.0) * 4.0 / width;
            double imag = (y - height / 2.0) * 4.0 / height;
            std::complex<double> c(real, imag);

            values[y][x] = mandelbrot(c);
        }
    }

    // Prepare the output image
    std::ofstream image("mandelbrot_set.ppm");
    image << "P3\n" << width << " " << height << " 255\n";

    // Write the output image in serial
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int value = values[y][x];
            int r = (value % 8) * 32;
            int g = (value % 16) * 16;
            int b = (value % 32) * 8;

            image << r << " " << g << " " << b << " ";
        }
        image << "\n";
    }

    image.close();
    std::cout << "Mandelbrot set image generated as mandelbrot_set.ppm." << std::endl;

    return 0;
}
