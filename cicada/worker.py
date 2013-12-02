#!/usr/bin/env python

import json
import logging
import sys
import time

from redis import Redis
from rq import Connection, Queue

from sourcecontrol import *
from shell import *
from publishers import *

from StateRedis import *
from libinjection_test import *

def utcnow():
    return int(time.time())

def timestamp():
    # remove microseconds, use a space
    s = datetime.datetime.utcnow().isoformat(' ')
    return s[0:19]


def pump():
    eventq = QUEUE_EVENT
    jobq = Queue(connection=Redis())
    now = utcnow()

    # GET ALL MESSAGES OFF EVENTQ
    events = set(eventq.event_get_all())

    logging.debug("got events %s", events)

    # now iterate through our tests, and find ones to
    # run.  this should be fast and non-blocking

    # for each listener, in each job, in each project
    for projectname, jobs in PROJECTS.iteritems():
        for jobname, job in jobs.iteritems():
            # set jobs
            eventq.jobs_put(projectname + '.' + jobname)

            for listener in job.get('listen', []):
                if listener.run(now, events):
                    job = jobq.enqueue(poll, projectname, jobname)
                    break

def poll(projectname, jobname):
    db = QUEUE_EVENT
    start = utcnow()
    worker = PROJECTS[projectname][jobname]
    workspace = os.path.join(WORKDIR, projectname, jobname)

    hkey = projectname + '.' + jobname
    db.job_set_key(hkey, 'started', utcnow())
    db.job_set_key(hkey, 'updated', utcnow())
    db.job_set_key(hkey, 'project', projectname)
    db.job_set_key(hkey, 'job',  jobname)
    db.job_set_key(hkey, 'state', 'running')

    if not os.path.exists(workspace):
        os.makedirs(workspace)

    output = []
    returncode = 0

    if 'source' in worker:
        output.append(timestamp() + ": Source @ {0}".format(workspace))
        (sout, serr, returncode) = worker['source'].run(workspace)

        if sout is not None and len(sout) > 0:
            output.append(sout)

        output.append(timestamp() + ": return code of {0}".format(returncode))

    if returncode == 0:
        output.append("{0}: {1}.{2}.{3}: {4}".format(timestamp(), projectname, jobname, start, "Execute"))
        (sout, serr, returncode) = worker['exec'].run(workspace)
        if output is not None and len(output) > 0:
            output.append(sout)
        output.append("{0}: {1}.{2}.{3}: {4}".format(timestamp(), projectname, jobname, start,
                                                     "return code of " + str(returncode)))

    if returncode == 0:
        state = 'pass'
    else:
        state = 'fail'

    msg = "{0}: {1}.{2}.{3}: {4}".format(timestamp(), projectname, jobname, start, state)
    output.append(msg)

    # write console output to disk
    # to workspace,
    with open(os.path.join(workspace, 'console.txt'), 'w') as fd:
        fd.write('\n'.join(output))

    outputs = []
    for pub in worker.get('publish', []):
        uri = pub.run(workspace, projectname, jobname, start)
        if uri:
            outputs.append(uri)

    db.job_set_key(hkey, 'updated', utcnow())
    db.job_set_key(hkey, 'state', state)

    return (state, outputs)
