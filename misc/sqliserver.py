#!/usr/bin/env python

#
#
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

class PageHandler(tornado.web.RequestHandler):
    def get(self, pagename):
        if pagename == '':
            pagename = 'home'
        try:
            self.render(pagename + ".html")
        except IOError:
            self.set_status(404)

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

        sqlstate = libinjection.sfilter()

        allfp = {}
        for name,values in self.request.arguments.iteritems():
            fps = []

            val = values[0]
            val = urllib.unquote(val)

            pat = libinjection.sqli_fingerprint(sqlstate, val, libinjection.CHAR_NULL, libinjection.COMMENTS_ANSI)
            issqli = bool(libinjection.sqli_blacklist(sqlstate))
            fps.append(['unquoted', 'ansi', issqli, pat])

            pat = libinjection.sqli_fingerprint(sqlstate, val, libinjection.CHAR_NULL, libinjection.COMMENTS_MYSQL)
            issqli = bool(libinjection.sqli_blacklist(sqlstate))
            fps.append(['unquoted', 'mysql', issqli, pat])

            pat =libinjection.sqli_fingerprint(sqlstate, val, libinjection.CHAR_SINGLE, libinjection.COMMENTS_ANSI)
            issqli = bool(libinjection.sqli_blacklist(sqlstate))
            fps.append(['single', 'ansi', issqli, pat])

            pat = libinjection.sqli_fingerprint(sqlstate, val, libinjection.CHAR_SINGLE, libinjection.COMMENTS_MYSQL)
            issqli = bool(libinjection.sqli_blacklist(sqlstate))
            fps.append(['single', 'mysql', issqli, pat])

            pat = libinjection.sqli_fingerprint(sqlstate, val, libinjection.CHAR_DOUBLE, libinjection.COMMENTS_MYSQL)
            issqli = bool(libinjection.sqli_blacklist(sqlstate))
            fps.append(['double', 'mysql', issqli, pat])

            allfp[name] = {
                'value': val,
                'fingerprints': fps
            }

        for name,values in self.request.arguments.iteritems():
            for val in values:
                # do it one more time include cut-n-paste was already url-encoded
                val = urllib.unquote(val)

                # swig returns 1/0, convert to True False
                issqli = bool(libinjection.is_sqli(sqlstate, val, None))

                # True if any issqli values are true
                qssqli = qssqli or issqli
                val = val.replace(',', ', ')

                pat = sqlstate.pat
                if not issqli:
                    pat = 'see below'
                args.append([name, val, issqli, pat])

        self.render("form.html",
                    title='libjection sqli diagnositc',
                    version = libinjection.LIBINJECTION_VERSION,
                    is_sqli=qssqli,
                    args=args,
                    allfp = allfp,
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
    (r"/([a-z]*)", PageHandler)
    ], **settings)


if __name__ == "__main__":

    import tornado.options
    #tornado.options.parse_config_file("/etc/server.conf")
    tornado.options.parse_command_line()

    server = wsgiref.simple_server.make_server('', 8888, application)
    server.serve_forever()

