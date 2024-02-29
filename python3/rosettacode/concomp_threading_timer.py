#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://rosettacode.org/wiki/Concurrent_computing#Python
"""
Display the strings "Enjoy" "Rosetta" "Code", one string per line, in random order.
"""

import threading
import random


def echo(text):
    print(text)


for text in ["Enjoy", "Rosetta", "Code"]:
    threading.Timer(random.random(), echo, (text,)).start()
