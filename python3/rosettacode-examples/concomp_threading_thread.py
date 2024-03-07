#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#threading.Thread
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

import random
import sys
import time
import threading

lock = threading.Lock()


def echo(s):
    time.sleep(1e-2*random.random())
    # use `.write()` with lock due to `print` prints empty lines occasionally
    with lock:
        sys.stdout.write(s)
        sys.stdout.write('\n')


for line in 'Enjoy Rosetta Code'.split():
    threading.Thread(target=echo, args=(line,)).start()
