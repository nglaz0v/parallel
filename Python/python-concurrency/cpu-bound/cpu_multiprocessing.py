#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process the required data (multiprocessing version)
"""

import multiprocessing
import time


def cpu_bound(number):
    """
    Compute the sum of the squares of each number from 0 to the passed-in value

    Somewhat silly function to create something that takes a long time to run on the CPU.
    """
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

"""
Little of this code had to change from the non-concurrent version. You had to
import multiprocessing and then just change from looping through the numbers to
creating a multiprocessing.Pool object and using its .map() method to send
individual numbers to worker-processes as they become free.

The processes optional parameter to the multiprocessing.Pool() constructor
deserves some attention. You can specify how many Process objects you want
created and managed in the Pool. By default, it will determine how many CPUs
are in your machine and create a process for each one. While this works great
for our simple example, you might want to have a little more control in a
production environment.

Also the multiprocessing.Pool code is built upon building blocks like Queue and
Semaphore that will be familiar to those of you who have done multithreaded and
multiprocessing code in other languages.
"""
