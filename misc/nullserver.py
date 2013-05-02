#!/usr/bin/env python

# A 'nullserver' that accepts input and generates output
# to trick sqlmap into thinking it's a database-driven site
#

import sys
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web

class ShutdownHandler(tornado.web.RequestHandler):
    def get(self):
        global fd
        fd.close()
        sys.exit(0)

class NullHandler(tornado.web.RequestHandler):

    def get(self):
        global fd
        param = self.request.query[3:]

        isint = False
        try:
            float(param)
            isint= True
        except ValueError:
            pass

        token = 'admin'
        if not isint and param != 'foo':
            token = ''
            fd.write(param + "\n")
            fd.flush()
        self.write("<html><head><title>ok</title></head><body>%s</body></html>" % (token,))

import os
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "yo mama sayz=",
    "xsrf_cookies": True,
    "gzip": True
}

application = tornado.web.Application([
    (r"/null", NullHandler),
    (r"/shutdown", ShutdownHandler),
    ], **settings)


if __name__ == "__main__":
    global fd
    fd = open('/tmp/urls.txt', 'w')

    import tornado.options
    #tornado.options.parse_config_file("/etc/server.conf")
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
