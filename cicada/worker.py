#!/usr/bin/env python

import sys
import time
import json

from sourcecontrol import *
from shell import *
from publishers import *

def now():
    return int(time.time())

def timestamp():
    # remove microseconds, use a space
    s = datetime.datetime.utcnow().isoformat(' ')
    return s[0:19]

def poll(projects, workdir, db, q):
    logging.info("See if there is anything to do")
    m = q.get()
    if m is None:
        logging.info("Nothing to do...")
        return True
    start = now()
    projectname, jobname = json.loads(m)

    logging.info("Got {0}.{1}".format(projectname, jobname))

    workspace = os.path.join(workdir, projectname, jobname)
    if not os.path.exists(workspace):
        os.makedirs(workspace)

    output = []

    try:
        worker = projects[projectname][jobname]
    except:
        logging.error("Got invalid job {0}.{1}".format(projectname, jobname))
        return False

    # inform DB we are working
    db.projectjobs_put(projectname, jobname, start, 'running', start)

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
    logging.info(msg)
    output.append(msg)

    # write console output to disk
    # to workspace,
    with open(os.path.join(workspace, 'console.txt'), 'w') as fd:
        fd.write('\n'.join(output))

    for pub in worker.get('publish', []):
        pub.run(workspace, projectname, jobname, start)

    db.projectjobs_put(projectname, jobname, start, state, now())
    db.jobhistory_put(projectname, jobname, start, state, now())

    # idle state
    return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(message)s")
    execfile('libinjection_test.py')
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)
    interval = 60*10

    if len(sys.argv) > 1:
        projectname = sys.argv[1]
        jobname = sys.argv[2]
        QUEUE_WORK.put(json.dumps( (projectname, jobname)))

    while True:
        if poll(PROJECTS, WORKDIR, DYNAMO, QUEUE_WORK):
            logging.info("Sleeping for {0} seconds".format(interval))
            time.sleep(interval)
