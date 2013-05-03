#!/usr/bin/env python

# A 'nullserver' that accepts input and generates output
# to trick sqlmap into thinking it's a database-driven site
#

import sys
import logging
import urllib
import libinjection
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import wsgiref.simple_server

def boring(arg):
    if arg == '':
        return True

    if arg == 'foo':
        return True

    if arg == 'NULL':
        return True

    try:
        float(arg)
        return True
    except ValueError:
        pass

    return False;

class NullHandler(tornado.web.RequestHandler):

    def get(self):
        #unquote = urllib.unquote
        #detectsqli = libinjection.detectsqli

        ids = self.request.arguments.get('id', [])
        if len(ids) == 1:
            formvalue = ids[0]
        else:
            formvalue = ''

        args = []
        extra = {}
        qssqli = False
        for name,values in self.request.arguments.iteritems():
            for val in values:
                # do it one more time include cut-n-paste was already url-encoded
                val = urllib.unquote(val)
                issqli = libinjection.detectsqli(val, extra)

                # True if any issqli values are true
                qssqli = qssqli or issqli
                val = val.replace(',', ', ')
                args.append([name, val, issqli, extra['fingerprint']])

        self.render("form.html",
                    version = libinjection.__version__,
                    is_sqli=qssqli,
                    args=args,
                    formvalue=formvalue
                    )

import os
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "."),
    "xsrf_cookies": False,
    "gzip": False
}

application = tornado.wsgi.WSGIApplication([
    (r"/diagnostics", NullHandler),
    ], **settings)


if __name__ == "__main__":

    import tornado.options
    #tornado.options.parse_config_file("/etc/server.conf")
    tornado.options.parse_command_line()

    server = wsgiref.simple_server.make_server('', 8888, application)
    server.serve_forever()

