#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using a Queue

The asyncio package provides queue classes that are designed to be similar to
classes of the queue module.

There is an alternative structure that can also work with async IO: a number of
producers, which are not associated with each other, add items to a queue. Each
producer may add multiple items to the queue at staggered, random, unannounced
times. A group of consumers pull items from the queue as they show up, greedily
and without waiting for any other signal.

In this design, there is no chaining of any individual consumer to a producer.
The consumers don’t know the number of producers, or even the cumulative number
of items that will be added to the queue, in advance.

It takes an individual producer or consumer a variable amount of time to put
and extract items from the queue, respectively. The queue serves as a
throughput that can communicate with the producers and consumers without them
talking to each other directly.

The synchronous version of this program would look pretty dismal: a group of
blocking producers serially add items to the queue, one producer at a time.
Only after all producers are done can the queue be processed, by one consumer
at a time processing item-by-item. There is a ton of latency in this design.
Items may sit idly in the queue rather than be picked up and processed
immediately.

An asynchronous version is below. The challenging part of this workflow is that
there needs to be a signal to the consumers that production is done. Otherwise,
await q.get() will hang indefinitely, because the queue will have been fully
processed, but consumers won’t have any idea that production is complete.
"""

import asyncio
import itertools as it
import os
import random
import time

async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()

async def randsleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)

async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")

async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()

async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

if __name__ == "__main__":
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
