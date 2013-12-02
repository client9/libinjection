#!/usr/bin/env python

import logging
import time

from worker import pump

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    while True:
        pump()
        time.sleep(60)
