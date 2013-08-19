#!/usr/bin/env python

"""
Mini script to take data files and make them "normal" for human reading
"""

from urlparse import parse_qsl
from urllib import unquote, unquote_plus


def qsv_normalize(s):
    while True:
        snew = unquote(s)
        if s == snew:
            return s
        s = snew

import sys
if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        print line
        print
        line = qsv_normalize(line)
        #line = line.replace("\n", ' ')
        print line
