// g++ -std=c++11 -pthread example.cc -o cpp_threads_demo

#include <iostream>
#include <thread>
#include <string>
#include <mutex>

std::mutex m; // will guard std::cout

void myfunction(const std::string &param)
{
    for (int i = 0; i < 10; i++) {
        // m.lock();
        std::lock_guard<std::mutex> lg(m);
        std::cout << "Executing function from a " << param << std::endl;
        // m.unlock();
    }
}

int main() {
    std::thread t1{ myfunction, "Thread 1" };
    std::thread t2{ myfunction, "Thread 2" };
    t1.join();
    t2.join();
}
