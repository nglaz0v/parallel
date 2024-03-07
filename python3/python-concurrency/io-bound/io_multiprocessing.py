#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloading web pages from a few sites (multiprocessing version)

$ pip3 install requests
"""

import requests
import multiprocessing
import time

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()


def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)


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
It’s enough for now to know that the synchronous, threading, and asyncio
versions of this example all run on a single CPU (because of GIL).

multiprocessing in the standard library was designed to break down that barrier
and run your code across multiple CPUs. At a high level, it does this by
creating a new instance of the Python interpreter to run on each CPU and then
farming out part of your program to run on it.

As you can imagine, bringing up a separate Python interpreter is not as fast as
starting a new thread in the current Python interpreter. It’s a heavyweight
operation and comes with some restrictions and difficulties, but for the
correct problem, it can make a huge difference.

The line that creates Pool is worth your attention. First off, it does not
specify how many processes to create in the Pool, although that is an optional
parameter. By default, multiprocessing.Pool() will determine the number of CPUs
in your computer and match that. This is frequently the best answer, and it is
in our case.

Next we have the initializer=set_global_session part of that call. Remember
that each process in our Pool has its own memory space. That means that they
cannot share things like a Session object. You don’t want to create a new
Session each time the function is called, you want to create one for each
process.
"""
