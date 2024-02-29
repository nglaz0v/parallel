// g++ -std=c++11 -pthread -o atomupd atomupd.cpp

// https://rosettacode.org/wiki/Atomic_updates#C++

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

#include <algorithm>
#include <array>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <random>
#include <thread>

using namespace std;

constexpr int bucket_count = 15;

void equalizer(array<int, bucket_count>& buckets,
               array<mutex, bucket_count>& bucket_mutex) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist_bucket(0, bucket_count - 1);

    while (true) {
        int from = dist_bucket(gen);
        int to = dist_bucket(gen);
        if (from != to) {
            lock_guard<mutex> lock_first(bucket_mutex[min(from, to)]);
            lock_guard<mutex> lock_second(bucket_mutex[max(from, to)]);
            int diff = buckets[from] - buckets[to];
            int amount = abs(diff / 2);
            if (diff < 0) {
                swap(from, to);
            }
            buckets[from] -= amount;
            buckets[to] += amount;
        }
    }
}

void randomizer(array<int, bucket_count>& buckets,
                array<mutex, bucket_count>& bucket_mutex) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist_bucket(0, bucket_count - 1);

    while (true) {
        int from = dist_bucket(gen);
        int to = dist_bucket(gen);
        if (from != to) {
            lock_guard<mutex> lock_first(bucket_mutex[min(from, to)]);
            lock_guard<mutex> lock_second(bucket_mutex[max(from, to)]);
            uniform_int_distribution<> dist_amount(0, buckets[from]);
            int amount = dist_amount(gen);
            buckets[from] -= amount;
            buckets[to] += amount;
        }
    }
}

void print_buckets(const array<int, bucket_count>& buckets) {
    int total = 0;
    for (const int& bucket : buckets) {
        total += bucket;
        cout << setw(3) << bucket << ' ';
    }
    cout << "= " << setw(3) << total << endl;
}

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(0, 99);

    array<int, bucket_count> buckets;
    array<mutex, bucket_count> bucket_mutex;
    for (int& bucket : buckets) {
        bucket = dist(gen);
    }
    print_buckets(buckets);

    thread t_eq(equalizer, ref(buckets), ref(bucket_mutex));
    thread t_rd(randomizer, ref(buckets), ref(bucket_mutex));

    while (true) {
        this_thread::sleep_for(chrono::seconds(1));
        for (mutex& mutex : bucket_mutex) {
            mutex.lock();
        }
        print_buckets(buckets);
        for (mutex& mutex : bucket_mutex) {
            mutex.unlock();
        }
    }
    return 0;
}
