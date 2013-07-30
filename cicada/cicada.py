#!/usr/bin/env python

import datetime
import logging
import os
import os.path
import multiprocessing
import subprocess
import time
import Queue
import tornado.httpserver
import tornado.web
import tornado.template
import tornado.escape

EVENTS = {}
STATUS = {}

def timestamp():
    # remove microseconds, use a space
    s = datetime.datetime.utcnow().isoformat(' ')
    return s[0:19]

class TestOnEvent(object):
    def __init__(self, event):
        self.event = event
    def run(self, events):
        return self.event in events

class TestOnTime(object):

    @staticmethod
    def parse_cronstring(pattern, rmax):
        if pattern == '*':
            return range(rmax)
        values = set()
        for parts in pattern.split(','):
            arange = [ int(i.strip()) for i in parts.split('-') ]
            if len(arange) == 1:
                values.add(arange[0])
            else:
                for i in range(arange[0], arange[1]):
                    values.add(i)
        ints = list(values)
        sorted(ints)
        return ints

    def __init__(self, minute='*', hour='*', dayofmonth='*', weekday='*'):
        self.minute     = TestOnTime.parse_cronstring(minute, 60)
        self.hour       = TestOnTime.parse_cronstring(hour, 24)
        self.dayofmonth = TestOnTime.parse_cronstring(dayofmonth, 32)
        self.weekday    = TestOnTime.parse_cronstring(weekday, 8)

    def run(self, event):
        now = datetime.datetime.utcnow()
        return now.minute in self.minute and \
            now.hour in self.hour and \
            now.day in self.dayofmonth and \
            now.weekday() in self.weekday

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

    def run(self, rootdir, test, status):
        name = test['name']
        destdir = os.path.join(os.path.join(rootdir, name));
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        link =  os.path.join(name, 'console.txt')
        linktext = 'console'
        fname = os.path.join(rootdir, link)
        logging.debug("Writing console to {0}".format(fname))
        with open(fname, 'w') as fd:
            fd.write(self.data)
        status['artifacts'].append( [
            options.urlprefix + "/artifacts/" + tornado.escape.url_escape(name) + "/console.txt",
            linktext
        ] )

class PublishArtifact(object):
    """
    Publish console ouput
    """

    def __init__(self, artifact, link, linktext):
        self.artifact = artifact
        self.link = link
        self.linktext = linktext

    def run(self, pubdir, test, status):
        name = test['name']
        destdir = os.path.join(os.path.join(pubdir, name));
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        subprocess.call(['cp', '-r', os.path.join(name, self.artifact), destdir])
        status['artifacts'].append( [
            options.urlprefix + '/artifacts/' +  tornado.escape.url_escape(name) + '/' + self.link,
            self.linktext
        ] )

class PublishStatus(object):
    """
    Publish project status
    """
    def __init__(self, templatepath):
        self.loader = tornado.template.Loader(".")

    def run(self, pubdir, tests, status):
        current = []
        for t in tests:
            current.append(status[t['name']])

        fname = os.path.join(pubdir, 'index.html')
        logging.debug("Writing status to {0}".format(fname))

        with open(fname, 'w') as fd:
            fd.write(self.loader.load('status.html').generate(status = current))

class HookShotHandler(tornado.web.RequestHandler):
    """
    something to handle github hookshots
    right now I'm just hardwiring it
    """
    def get(self):
        EVENTS['libinjection'] = True
    def post(self):
        EVENTS['libinjection'] = True

class KickHandler(tornado.web.RequestHandler):
    """
    hack to do everything
    """
    def get(self):
        EVENTS['kick'] = True

class CicadaStatusHandler(tornado.web.RequestHandler):
    def get(self):
        current = STATUS.values()
        current = sorted(current, key=lambda x: x['order'])
        self.render(
            'status.html',
            status=current,
            ssl_protocol=self.request.headers.get('X-SSL-Protocol', ''),
            ssl_cipher=self.request.headers.get('X-SSL-Cipher', '')
        )

class Cicada(object):
    def __init__(self, tests):
        global STATUS
        global EVENTS

        EVENTS = {
            'kick': 1
        }

        self.tests = tests
        workspace = options.workspace
        pubspace = options.artifacts

        logging.info("Using workspace: " + workspace)
        logging.info("Using artifacts: " + pubspace)

        if not os.path.exists(workspace):
            logging.debug('making directory ' + workspace)
            os.makedirs(workspace)

        if not os.path.exists(pubspace):
            logging.debug('making directory ' + pubspace)
            os.makedirs(pubspace)


        self.workqueue = multiprocessing.Queue()
        self.statusqueue = multiprocessing.Queue()

        num_workers = options.workers
        logging.debug("NUM WORKERS " + str(num_workers))
        workers = [ multiprocessing.Process(target=buzz,
                                            args=(self.workqueue, self.statusqueue, workspace, pubspace))
                    for i in range(num_workers) ]
        for w in workers:
            w.start()

        count  = 0
        for t in tests:
            STATUS[t['name']] = {
                'name'        : t['name'],
                'status'      : 'initial',
                'timestamp'   : timestamp(),
                'artifacts'   : [],
                'duration'    : 0,
                'order'       : count
            }
            count += 1


        application = make_tornado_application(pubspace)
        os.chdir(workspace)

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)

        self.poll()

        # http://stackoverflow.com/questions/12479054/how-to-run-functions-outside-websocket-loop-in-python-tornado
        main_loop = tornado.ioloop.IOLoop.instance()
        pc = tornado.ioloop.PeriodicCallback(self.poll, 60* 1000)
        pc.start()
        rs = tornado.ioloop.PeriodicCallback(self.receive_status, 1 * 1000)
        rs.start()
        main_loop.start()

    def receive_status(self):
        global STATUS
        # update current status messages
        try:
            while True:
                msg = self.statusqueue.get_nowait()
                logging.debug("Got status: {0}".format(msg))
                STATUS[msg['name']]= msg
        except Queue.Empty:
            pass

    def poll(self):
        global EVENTS
        logging.debug("See if we can run tests ...")
        # now iterate through our tests, and find ones to
        # run.  this should be fast and non-blocking

        for t in self.tests:
            run = False
            if 'listen' in t and len(t['listen']) > 0:
                for listener in t['listen']:
                    if listener.run(EVENTS):
                        logging.debug("{0} ok!".format(listener))
                        run = True
                        break
                    else:
                        pass
                        #logging.debug("{0} rejected".format(listener))
            if run or 'kick' in EVENTS:
                logging.debug("Adding {0} to be built".format(t['name']))
                self.workqueue.put( (t, STATUS[t['name']] ))
        EVENTS = {}

def buzz(workqueue, statusqueue, workspace, pubspace):
    try:
        while True:
            msg = workqueue.get(block=True, timeout=None)
            runtest(statusqueue, workspace, pubspace, msg[0],msg[1])
    except Queue.Empty:
        pass


def runtest(statusqueue, workspace, pubspace, t, statusmsg):
    t0 = time.time()

    output = []

    statusmsg['timestamp'] = timestamp()
    statusmsg['status']    = 'running'
    statusmsg['duration']  = 0
    statusmsg['artifacts'] = []
    statusqueue.put(statusmsg)

    output.append(timestamp() + ": Source\n")

    (sout, serr, returncode) = t['source'].run(t['name'])
    output.append(sout)

    if returncode != 0:
        output.append(timetime() + ": return code of {0}".format(returncode))
        statusmsg['timestamp'] = timestamp()
        statusmsg['status'] = 'fail'
        statusqueue.put(statusmsg)
        output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Fail"))
    else:
        output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Execute"))
        (sout, serr, returncode) = t['exec'].run(t['name'])
        output.append(sout)
        if returncode != 0:
            output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "return code of " + str(returncode)))
            statusmsg['status'] = 'fail'
            output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Fail"))
        else:
            statusmsg['status'] = 'pass'
            output.append("{0}: {1}: {2}\n".format(timestamp(), t['name'], "Pass"))

    statusmsg['timestamp'] = timestamp()
    statusmsg['duration'] = int(time.time() - t0)

    # publish test console output and result
    pubcon = PublishConsole('\n'.join(output))
    pubcon.run(pubspace, t, statusmsg)

    if 'publish' in t:
        for pub in t['publish']:
            pub.run(pubspace, t, statusmsg)

    statusqueue.put(statusmsg)

def make_tornado_application(pubspace):
    settings = {
        "static_path": pubspace,
        "template_path": os.getcwd(),
        "xsrf_cookies": False,
        "gzip": options.gzip,
        'debug': True
    }

    handlers = [
        (options.urlprefix + '/hookshot', HookShotHandler),
        (options.urlprefix + '/kick', KickHandler),
        (options.urlprefix + '/$', CicadaStatusHandler),
        (options.urlprefix + '/index.html', CicadaStatusHandler),
        (options.urlprefix + '/artifacts/(.*)', tornado.web.StaticFileHandler, {'path': pubspace})
    ]

    return  tornado.web.Application(handlers, **settings)

from tornado.options import define, options

#
# web related options
#
define("port", default=9000, help="HTTP port")
define("gzip", default=False, help="gzip output, not needed if running behind a proxy")
define("urlprefix", default="/cicada", help="url prefix")

#
# test related options
#
define("workers", default=2, help="Number of test workers processes")
define("workspace", default= os.path.expanduser("~/cicada/workspace"),
       help="where data is read (where source code is)")
define("artifacts", default = os.path.expanduser("~/cicada/artifacts"),
       help="where data is written (where results are published)")


if __name__ == '__main__':
    tornado.options.parse_command_line()

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(process)d %(message)s")

    execfile('libinjection_test.py')

    c = Cicada(tests)
