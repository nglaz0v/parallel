#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#multiprocessing
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

from __future__ import print_function
from multiprocessing import Pool


def main():
    p = Pool()
    p.map(print, 'Enjoy Rosetta Code'.split())


if __name__ == "__main__":
    main()
