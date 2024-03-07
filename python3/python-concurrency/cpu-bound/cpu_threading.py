#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process the required data (synchronous version)
"""

import concurrent.futures
import time


def cpu_bound(number):
    """
    Compute the sum of the squares of each number from 0 to the passed-in value

    Somewhat silly function to create something that takes a long time to run on the CPU.
    """
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(cpu_bound, numbers)


if __name__ == "__main__":
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

"""
How much do you think rewriting this code using threading or asyncio will speed
this up?
If you answered “Not at all,” give yourself a cookie.
If you answered, “It will slow it down,” give yourself two cookies.

Here’s why: In your I/O-bound example above, much of the overall time was spent
waiting for slow operations to finish. threading and asyncio sped this up by
allowing you to overlap the times you were waiting instead of doing them
sequentially.

On a CPU-bound problem, however, there is no waiting. The CPU is cranking away
as fast as it can to finish the problem. In Python, both threads and tasks run
on the same CPU in the same process. That means that the one CPU is doing all
of the work of the non-concurrent code plus the extra work of setting up
threads or tasks.
"""
