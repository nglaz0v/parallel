#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#Python
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

import asyncio


async def print_(string: str) -> None:
    print(string)


async def main():
    strings = ['Enjoy', 'Rosetta', 'Code']
    coroutines = map(print_, strings)
    await asyncio.gather(*coroutines)


if __name__ == '__main__':
    asyncio.run(main())
