#!/usr/bin/env python
#  Copyright 2012, Nick Galbreath
#  nickg@client9.com
#  GPL v2 License -- Commericial Licenses available.
#  http://www.gnu.org/licenses/gpl-2.0.txt
#
from sqlparse_exploits import byline
from multiprocessing import Pool
from glob import glob
import sys
import logging

def f(fname):
    logging.debug("opening " + fname)
    with open(fname, 'r') as fd:
        byline(fd, sys.stdout)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    files = glob('/Users/ngalbreath/urlparts/*')

    pool = Pool(processes=2)
    pool.map(f, glob('/Users/ngalbreath/urlparts/*'))
