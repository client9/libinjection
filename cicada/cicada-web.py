#!/usr/bin/env python

import logging
import os
import os.path
import time

import tornado.httpserver
import tornado.web
import tornado.template
import tornado.escape

execfile('libinjection_test.py')

def epoch_to_ago(ago, now=0):
    if now == 0:
        now = int(time.time())
    diff = now - ago
    if (diff < 0):
        return "future"
    if (diff < 2):
        return "now"
    if (diff < 60):
        return "{0}sec".format(diff)
    if (diff < 60*60*3):
        return "{0}min".format(int(diff / 60.0))
    if (diff < 86400):
        return "{0}hr".format(int(diff / 3600.0))
    return "{0}day".format(int(diff / 86400.0))

class HookShotHandler(tornado.web.RequestHandler):
    """
    something to handle github hookshots
    right now I'm just hardwiring it
    """
    def get(self):
        QUEUE_EVENT.event_put('libinjection')
    def post(self):
        QUEUE_EVENT.event_put('libinjection')

class KickHandler(tornado.web.RequestHandler):
    """
    hack to do everything
    """
    def get(self):
        QUEUE_EVENT.event_put('libinjection')


class CicadaStatusHandler(tornado.web.RequestHandler):
    def get(self):
        now = int(time.time())
        projects = {}
        for jobname in QUEUE_EVENT.jobs_get_all():
            rs = QUEUE_EVENT.job_get(jobname)
            try:
                projectname = str(rs['project'])
                jobname = str(rs['job'])
                artifacts = []
                publishers = PROJECTS[projectname][jobname].get('publish', [])
                for p in publishers:
                    href, text = p.link()
                    href = "artifacts/{0}/{1}/{2}/{3}".format(projectname, jobname, rs['started'], href)
                    artifacts.append( (href, text) )
                job = {
                    'project': projectname,
                    'job': jobname,
                    'start': int(rs['started']),
                    'ago': epoch_to_ago(int(rs['started']), now),
                    'duration': int(rs['updated']) - int(rs['started']),
                    'state': str(rs['state']),
                    'artifacts': artifacts
                }

                if rs['project'] in projects:
                    projects[rs['project']].append(job)
                else:
                    projects[rs['project']] = [ job ]
            except KeyError, e:
                logging.error("Likely dead project:  {0} {1}".format(e, rs))

            #except Exception, e:
            #    logging.error("Problem in rendering: {0} {1}".format(e, rs))


        self.render(
            'status.html',
            status=projects,
            ssl_protocol=self.request.headers.get('X-SSL-Protocol', ''),
            ssl_cipher=self.request.headers.get('X-SSL-Cipher', '')
        )

class Cicada(object):
    def __init__(self):
        application = make_tornado_application(PUBDIR)
        os.chdir(WORKDIR)

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

def make_tornado_application(pubspace):
    settings = {
        "static_path": pubspace,
        "template_path": os.getcwd(),
        "xsrf_cookies": False,
        "gzip": options.gzip,
        'debug': True
    }

    handlers = [
        (options.urlprefix + '/$', CicadaStatusHandler),
        (options.urlprefix + '/index.html', CicadaStatusHandler),
        (r'/bootstrap/(.*)', tornado.web.StaticFileHandler, {'path': '/opt/bootstrap' }),
        (r'/jquery/(.*)', tornado.web.StaticFileHandler, {'path': '/opt/jquery' }),
        (options.urlprefix + '/artifacts/(.*)', tornado.web.StaticFileHandler, {'path': pubspace}),
        (options.urlprefix + '/hookshot', HookShotHandler),
        (options.urlprefix + '/kick', KickHandler)
    ]

    return  tornado.web.Application(handlers, **settings)

from tornado.options import define, options

#
# web related options
#
define("port", default=9000, help="HTTP port")
define("gzip", default=False, help="gzip output, not needed if running behind a proxy")
define("urlprefix", default="/cicada", help="url prefix")

if __name__ == '__main__':
    tornado.options.parse_command_line()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(message)s")
    c = Cicada()
