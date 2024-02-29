#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Atomic_updates#Python
"""
Define a data type consisting of a fixed number of 'buckets', each
containing a nonnegative integer value, which supports operations to:
- get the current value of any bucket
- remove a specified amount from one specified bucket and add it to
  another, preserving the total of all bucket values, and clamping
  the transferred amount to ensure the values remain non-negative
In order to exercise this data type, create one set of buckets, and
start three concurrent tasks:
- As often as possible, pick two buckets and make their values closer
  to equal.
- As often as possible, pick two buckets and arbitrarily redistribute
  their values.
- At whatever rate is convenient, display (by any means) the total
  value and, optionally, the individual values of each bucket.
The display task need not be explicit; use of e.g. a debugger or
trace tool is acceptable provided it is simple to set up to provide
the display.
This task is intended as an exercise in atomic operations. The sum of
the bucket values must be preserved even if the two tasks attempt to
perform transfers simultaneously, and a straightforward solution is
to ensure that at any time, only one transfer is actually occurring —
that the transfer operation is atomic.
"""

from __future__ import with_statement  # required for Python 2.5
import threading
import random
import time

terminate = threading.Event()


class Buckets:
    def __init__(self, nbuckets):
        self.nbuckets = nbuckets
        self.values = [random.randrange(10) for i in range(nbuckets)]
        self.lock = threading.Lock()

    def __getitem__(self, i):
        return self.values[i]

    def transfer(self, src, dst, amount):
        with self.lock:
            amount = min(amount, self.values[src])
            self.values[src] -= amount
            self.values[dst] += amount

    def snapshot(self):
        # copy of the current state (synchronized)
        with self.lock:
            return self.values[:]


def randomize(buckets):
    nbuckets = buckets.nbuckets
    while not terminate.isSet():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst != src:
            amount = random.randrange(20)
            buckets.transfer(src, dst, amount)


def equalize(buckets):
    nbuckets = buckets.nbuckets
    while not terminate.isSet():
        src = random.randrange(nbuckets)
        dst = random.randrange(nbuckets)
        if dst != src:
            amount = (buckets[src] - buckets[dst]) // 2
            if amount >= 0:
                buckets.transfer(src, dst, amount)
            else:
                buckets.transfer(dst, src, -amount)


def print_state(buckets):
    snapshot = buckets.snapshot()
    for value in snapshot:
        print('%2d' % value)
    print('=', sum(snapshot))


# create 15 buckets
buckets = Buckets(15)

# the randomize thread
t1 = threading.Thread(target=randomize, args=[buckets])
t1.start()

# the equalize thread
t2 = threading.Thread(target=equalize, args=[buckets])
t2.start()

# main thread, display
try:
    while True:
        print_state(buckets)
        time.sleep(1)
except KeyboardInterrupt:  # ^C to finish
    terminate.set()

# wait until all worker threads finish
t1.join()
t2.join()
