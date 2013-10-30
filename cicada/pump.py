#!/usr/bin/env python

import datetime
import time
import json
from sourcecontrol import *
from shell import *
from publishers import *
from events import *

def timestamp():
    # remove microseconds, use a space
    s = datetime.datetime.utcnow().isoformat(' ')
    return s[0:19]

class Pump(object):
    def __init__(self, projects, eventq, workq):
        self.projects = projects
        self.eventq = eventq
        self.workq = workq

    def run(self):
        # GET ALL MESSAGES OFF EVENTQ
        events = set(self.eventq.get_all())

        logging.info("See if we can run tests ...")

        # now iterate through our tests, and find ones to
        # run.  this should be fast and non-blocking

        now = int(time.time())
        for projectname, jobs in self.projects.iteritems():
            for jobname, job in jobs.iteritems():
                run = False
                for listener in job.get('listen', []):
                    if listener.run(now, events):
                        #logging.info("{0} ok!".format(listener))
                        run = True
                        break
                    else:
                        pass
                        #logging.debug("{0} rejected".format(listener))
                if run:
                    logging.info("Adding {0}.{1} to be built".format(projectname, jobname))
                    self.workq.put(json.dumps( (projectname, jobname) ))


import logging
import time
from QueueAWS import QueueAWS

if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(message)s")

    execfile('libinjection_test.py')
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)

    if len(sys.argv) > 1:
        eventname = sys.argv[1]
        QUEUE_EVENT.put(eventname)

    p = Pump(PROJECTS, QUEUE_EVENT, QUEUE_WORK)
    interval = 10
    while (True):
        p.run()
        time.sleep(interval)
