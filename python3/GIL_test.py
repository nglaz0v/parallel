#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Parallel Programming Cookbook
Evaluating the performance of multithread applications

We will verify the impact of the Global Interpreter Lock (GIL), evaluating the
performance of a multithread application. The GIL is the lock introduced by the
CPython interpreter. The GIL prevents parallel execution of multiple threads in
the interpreter. Before being executed each thread must wait for the GIL to
release the thread that is running. In fact, the interpreter forces the
executing thread to acquire the GIL before it accesses anything on the
interpreter itself as the stack and instances of Python objects. This is
precisely the purpose of GIL—it prevents concurrent access to Python objects
from different threads. The GIL then protects the memory of the interpreter and
makes the garbage work in the right manner. The fact is that the GIL prevents
the programmer from improving the performance by executing threads in parallel.
If we remove the GIL from the CPython interpreter, the threads would be
executed in parallel. The GIL does not prevent a process from running on a
different processor, it simply allows only one thread at a time to turn inside
the interpreter.

Let's remember that you do not add threads to speed up the startup time of an
application, but to add support to the concurrence. For example, it's useful to
create a pool of threads once and then reuse the worker. This allows us to
split a big dataset and run the same function on different parts (the
producer/consumer model). So, although it is not the norm for concurrent
applications, these tests are designed to be simple. Is the GIL an obstacle for
those who work on pure Python and try to exploit multi-core hardware
architectures? Yes it does. While threads are a language construct, the CPython
interpreter is the bridge between the threads and operating system. This is why
Jython, IronPython, and others interpreters do not possess GIL, as it was
simply not necessary and it has not been reimplemented in the interpreter.
"""

import sys
from threading import Thread


def test1():
    """
    If we look at the results, we see how the thread calls are more expensive
    than the calls without threads. In particular, we also note how the cost of
    adding the thread is proportional to their number.
    """
    # empty function
    pass


def test2():
    """
    As we can see from the output, we get no advantage by increasing the number
    of threads. The function is executed in Python and because of the overhead
    for creating threads and GIL, the multithreaded example can never be faster
    than the non-threaded example. Again, let's remember that the GIL allows
    only one thread at a time to access the interpreter.
    """
    # calculate the brute force of the Fibonacci sequence
    a, b = 0, 1
    for i in range(10000):
        a, b = b, a + b


def test3():
    """
    We have begun to see a better result in the multithreading case. In
    particular, we've noted how the threaded execution is half time-consuming
    if we compare it with the non_threaded one. Let's remember that in real
    life, we would not use threads as a benchmark. Typically, we would put the
    threads in a queue, pull them out, and perform other tasks. Having multiple
    threads that execute the same function although useful in certain cases, is
    not a common use case for a concurrent program, unless it divides the data
    in the input.
    """
    # reading 1,000 times a block of data (1Kb) from the file
    fh = open(sys.argv[0], "rb")
    size = 1024
    for i in range(1000):
        fh.read(size)


def test4():
    """
    As you can see, during the I/O, the GIL is released. The multithreading
    execution becomes faster than the single-threaded execution. Since many
    applications perform a certain amount of work in the I/O, the GIL does not
    prevent a programmer from creating a multithreading work that concurrently
    increases the speed of execution.
    """
    # try to get to the URL and simply read the first 1k bytes of it
    import urllib.request
    for i in range(10):
        with urllib.request.urlopen("https://www.packtpub.com/")as f:
            f.read(1024)


function_to_run = (test1, test2, test3, test4)
k = int(sys.argv[1])-1


class threads_object(Thread):
    def run(self):
        function_to_run[k]()


class nothreads_object(object):
    def run(self):
        function_to_run[k]()


def non_threaded(num_iter):
    funcs = []
    for i in range(int(num_iter)):
        funcs.append(nothreads_object())
    for i in funcs:
        i.run()


def threaded(num_threads):
    funcs = []
    for i in range(int(num_threads)):
        funcs.append(threads_object())
    for i in funcs:
        i.start()
    for i in funcs:
        i.join()


def show_results(func_name, results):
    print("%-23s %4.6f seconds" % (func_name, results))


if __name__ == "__main__":
    from timeit import Timer

    repeat = 100
    number = 1
    num_threads = [1, 2, 4, 8]

    print('Starting tests')
    for i in num_threads:
        t = Timer("non_threaded(%s)" % i, "from __main__ import non_threaded")
        best_result = min(t.repeat(repeat=repeat, number=number))
        show_results("non_threaded (%s iters)" % i, best_result)

        t = Timer("threaded(%s)" % i, "from __main__ import threaded")
        best_result = min(t.repeat(repeat=repeat, number=number))
        show_results("threaded (%s threads)" % i, best_result)
    print('Iterations complete')
