#!/usr/bin/python

import sys

from bloom_filter import BloomFilter

have_seen = BloomFilter(max_elements=1000000000)

for line in sys.stdin:
    phrase=line.rstrip()
    if not phrase in have_seen:
        have_seen.add(phrase)
        print(phrase)
