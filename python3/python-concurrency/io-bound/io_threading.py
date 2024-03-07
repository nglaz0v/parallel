#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloading web pages from a few sites (threading version)

$ pip3 install requests
"""

import concurrent.futures
import requests
import threading
import time


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")

"""
Those of you coming from other languages, or even Python 2, are probably
wondering where the usual objects and functions are that manage the details
you’re used to when dealing with threading, things like
Thread.start(), Thread.join(), and Queue.

These are all still there, and you can use them to achieve fine-grained control
of how your threads are run. But, starting with Python 3.2, the standard
library added a higher-level abstraction called Executors that manage many of
the details for you if you don’t need that fine-grained control.

The other interesting change in our example is that each thread needs to create
its own requests.Session() object. When you’re looking at the documentation for
requests, it’s not necessarily easy to tell, but reading
[this issue](https://github.com/requests/requests/issues/2766), it seems fairly
clear that you need a separate Session for each thread.

This is one of the interesting and difficult issues with threading. Because the
operating system is in control of when your task gets interrupted and another
task starts, any data that is shared between the threads needs to be protected,
or thread-safe. Unfortunately requests.Session() is not thread-safe.

There are several strategies for making data accesses thread-safe depending on
what the data is and how you’re using it. One of them is to use thread-safe
data structures like Queue from Python’s queue module.

These objects use low-level primitives like threading.Lock to ensure that only
one thread can access a block of code or a bit of memory at the same time. You
are using this strategy indirectly by way of the ThreadPoolExecutor object.

Another strategy to use here is something called thread local storage.
threading.local() creates an object that looks like a global but is specific to
each individual thread. In your example, this is done with thread_local and
get_session(). thread_local itself takes care of separating accesses from
different threads to different data.

When get_session() is called, the session it looks up is specific to the
particular thread on which it’s running. So each thread will create a single
session the first time it calls get_session() and then will simply use that
session on each subsequent call throughout its lifetime.

Finally, a quick note about picking the number of threads. The difficult answer
here is that the correct number of threads is not a constant from one task to
another. Some experimentation is required.
"""
