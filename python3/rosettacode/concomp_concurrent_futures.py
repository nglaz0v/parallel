#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#Python
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

from concurrent import futures


if __name__ == '__main__':
    with futures.ProcessPoolExecutor() as executor:
        _ = list(executor.map(print, 'Enjoy Rosetta Code'.split()))
