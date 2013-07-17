#!/usr/bin/env python

import datetime
import logging
import os
import os.path
import subprocess
import time

import tornado.template


def timestamp():
    # remove microseconds, use a space
    s = datetime.datetime.utcnow().isoformat(' ')
    return s[0:19]

class CheckoutGit(object):
    """
    does a pull or clone from a git repo as needed
    """

    def __init__(self, url):
        self.url = url

    def run(self, name):
        if os.path.exists(name):
            cwd = name
            cmd = ['git', 'pull']
            logging.info("{0}: git pull (from {1})".format(name, self.url))
        else:
            cwd = None
            cmd = ['git', 'clone', self.url, name, '--depth', '1']
            logging.info("{0}: git clone {1} {2}".format(name, self.url, name))

        p = subprocess.Popen(cmd,
                             cwd=cwd,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)

        (sout,serr) = p.communicate()
        return (sout,serr,p.returncode)

class ExecuteShell(object):
    """
    Executes a bash script
    """
    def __init__(self, script):
        self.script = script

    def run(self, name):
        p = subprocess.Popen(['/bin/bash', '-v', '-c', self.script],
                             cwd=name,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             shell=False)
        (sout, serr) = p.communicate()

        return (sout, serr, p.returncode)

class PublishConsole(object):
    """
    Publish console ouput
    """

    def __init__(self, console):
        self.data = console

    def run(self, rootdir, name):
        fname = os.path.join(rootdir, name + '.txt')
        logging.debug("Writing console to {0}".format(fname))
        with open(fname, 'w') as fd:
            fd.write(self.data)

class PublishArtifact(object):
    """
    Publish console ouput
    """

    def __init__(self, artifact):
        self.data = artifact

    def run(self, pubdir, name):
        destdir = os.path.join(os.path.join(pubdir, name));
        if not os.exists(destdir):
            os.makedirs(name)

        subprocess.call(['cp', '-r', self.artifact, destdir])

class PublishStatus(object):
    """
    Publish project status
    """
    def __init__(self, templatepath):
        self.loader = tornado.template.Loader(".")

    def run(self, pubdir, tests):
        status = []
        for t in tests:
            status.append(t['status'])

        fname = os.path.join(pubdir, 'index.html')
        logging.debug("Writing status to {0}".format(fname))

        with open(fname, 'w') as fd:
            fd.write(self.loader.load('status.html').generate(status = status))

def cicada(workspace, pubspace, tests):
    """
    Run a test project
    """

    if not os.path.exists(workspace):
        logging.debug('making directory ' + workspace)
        os.makedirs(workspace)
    if not os.path.exists(pubspace):
        logging.debug('making directory ' + pubspace)
        os.makedirs(pubspace)

    pubstatus = PublishStatus(os.getcwd())

    os.chdir(workspace)

    status = []
    for t in tests:
        t['status'] = {
            'name'        : t['name'],
            'status'      : 'pending',
            'timestamp'   : timestamp(),
            'duration'    : 0
        }

    pubstatus.run(pubspace, tests)

    for t in tests:
        t0 = time.time()

        output = []

        t['status']['timestamp'] = timestamp()
        t['status']['status']    = 'running'
        t['status']['duration']  = 0;

        pubstatus.run(pubspace, tests)

        output.append(timestamp() + ": Source\n")

        (sout, serr, returncode) = t['source'].run(t['name'])
        output.append(sout)

        if returncode != 0:
            output.append(timetime() + ": return code of {0}".format(returncode))
            t['status']['timestamp'] = timestamp()
            t['status']['status'] = 'fail'
            output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Fail"))
        else:
            output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Execute"))
            (sout, serr, returncode) = t['exec'].run(t['name'])
            output.append(sout)
            if returncode != 0:
                output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "return code of " + str(returncode)))
                t['status']['timestamp'] = timestamp()
                t['status']['status'] = 'fail'
                output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Fail"))
            else:
                t['status']['timestamp'] = timestamp()
                t['status']['status'] = 'pass'
                output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Pass"))

        t['status']['duration'] = int(time.time() - t0)

        if 'publish' in t:
            for pub in ['publish']:
                pub.run(pubspace, pub['name'])

        # publish test console output and result
        pubcon = PublishConsole('\n'.join(output))
        pubcon.run(pubspace, t['name'])


    # publish final status
    pubstatus.run(pubspace, tests)
