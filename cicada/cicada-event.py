#!/usr/bin/env python

import logging
import sys
from StateRedis import StateRedis

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    connection = StateRedis()
    eventname = sys.argv[1]
    logging.debug("Adding event %s", eventname)
    connection.event_put(eventname)
