// g++ -std=c++11 -pthread -D_GLIBCXX_USE_NANOSLEEP -o concomp concomp.cpp

// https://rosettacode.org/wiki/Concurrent_computing#C++

/* Display the strings "Enjoy" "Rosetta" "Code", one string per line, in
 * random order.
 */

#include <thread>
#include <iostream>
#include <vector>
#include <random>
#include <chrono> 

int main()
{
  std::random_device rd;
  std::mt19937 eng(rd()); // mt19937 generator with a hardware random seed.
  std::uniform_int_distribution<> dist(1,1000);
  std::vector<std::thread> threads;

  for(const auto& str: {"Enjoy\n", "Rosetta\n", "Code\n"}) {
    // between 1 and 1000ms per our distribution
    std::chrono::milliseconds duration(dist(eng)); 

    threads.emplace_back([str, duration](){                                                                    
      std::this_thread::sleep_for(duration);
      std::cout << str;
    });
  }

  for(auto& t: threads) t.join(); 

  return 0;
}
