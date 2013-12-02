#!/usr/bin/env python

import logging
import time

import cicada

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    while True:
        cicada.pump()
        time.sleep(60)
