#!/usr/bin/env python

"""
Mini script to url encode data
"""

from urllib import quote

import sys
if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        print quote(line)
