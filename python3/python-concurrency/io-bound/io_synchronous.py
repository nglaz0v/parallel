#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloading web pages from a few sites (synchronous version)

$ pip3 install requests
"""

import requests
import time


def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


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
It is possible to simply use get() from requests directly, but creating a
Session object allows requests to do some fancy networking tricks and really
speed things up.
"""
