#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#gevent
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

from __future__ import print_function
import random
import gevent

delay = lambda: 1e-4*random.random()
gevent.joinall([gevent.spawn_later(delay(), print, line)
               for line in 'Enjoy Rosetta Code'.split()])
