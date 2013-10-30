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

class HookShotHandler(tornado.web.RequestHandler):
    """
    something to handle github hookshots
    right now I'm just hardwiring it
    """
    def get(self):
        DYNAMO.put('libinjection')
    def post(self):
        DYNAMO.put('libinjection')

class KickHandler(tornado.web.RequestHandler):
    """
    hack to do everything
    """
    def get(self):
        DYNAMO.put('libinjection')

class CicadaStatusHandler(tornado.web.RequestHandler):
    def get(self):
        projects = {}
        for rs in DYNAMO.projectjobs_list_all():
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
                    'duration': int(rs['updated'] - rs['started']),
                    'state': str(rs['state']),
                    'artifacts': artifacts
                }


                if rs['project'] in projects:
                    projects[rs['project']].append(job)
                else:
                    projects[rs['project']] = [ job ]
            except Exception, e:
                logging.error("Problem in rendering: {0} {1}".format(e, rs))


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

if __name__ == '__main__':
    tornado.options.parse_command_line()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(message)s")
    c = Cicada()
