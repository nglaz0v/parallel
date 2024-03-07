#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloading web pages from a few sites (asyncio version)

$ pip3 install aiohttp
"""

import asyncio
import time
import aiohttp


async def download_site(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    # asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    asyncio.run(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")

"""
An important point of asyncio is that the tasks never give up control without
intentionally doing so. They never get interrupted in the middle of an
operation. This allows us to share resources a bit more easily in asyncio than
in threading. You don’t have to worry about making your code thread-safe.

Any function that calls await needs to be marked with async.

In this example you can share the session across all tasks, so the session is
created here as a context manager. The tasks can share the session because they
are all running on the same thread. There is no way one task could interrupt
another while the session is in a bad state.

Inside that context manager, it creates a list of tasks using
asyncio.ensure_future(), which also takes care of starting them. Once all the
tasks are created, this function uses asyncio.gather() to keep the session
context alive until all of the tasks have completed.

One of the cool advantages of asyncio is that it scales far better than
threading. Each task takes far fewer resources and less time to create than a
thread, so creating and running more of them works well. This example just
creates a separate task for each site to download, which works out quite well.
"""
