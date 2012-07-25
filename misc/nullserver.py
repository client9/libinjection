#!/usr/bin/env python

# A 'nullserver' that accepts input and generates output
# to trick sqlmap into thinking it's a database-driven site
#

import sys
import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.database
import random
import hashlib

def hack(id, query):
    global fd
    isint = False
    try:
        float(id)
        isint= True
    except ValueError:
        pass
    if not isint and id != 'foo':
        token = ''
        fd.write(id + "\n")
        fd.flush()

    sql = query % (id)
    try:
        return db.get(sql)
    except:
        return None

class ShutdownHandler(tornado.web.RequestHandler):
    def get(self):
        global fd
        fd.close()
        sys.exit(0)

class Type1(tornado.web.RequestHandler):
    def get(self):

        id = self.get_argument("id")
        sql = "SELECT * FROM junkusers WHERE id = %s"
        row = hack(id, sql)

        if row:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % (row['name'],))
        else:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % ('ooops',))

class Type2(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id")
        sql = "SELECT * FROM junkusers WHERE id = '%s'"
        row = hack(id, sql)
        if row:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % (row['name'],))
        else:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % ('ooops',))

class Type3(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id")
        sql = "SELECT * FROM junkusers WHERE id = \"%s\""
        row = hack(id, sql)
        if row:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % (row['name'],))
        else:
            self.write("<html><head><title>ok</title></head><body>%s</body></html>" % ('ooops',))



class NullHandler(tornado.web.RequestHandler):

    def get(self):
        global fd
        param = self.request.query[3:]
        m = hashlib.md5()
        m.update(param)

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
    (r"/type1", Type1),
    (r"/type2", Type2),
    (r"/type3", Type3),
    (r"/shutdown", ShutdownHandler),
    ], **settings)


if __name__ == "__main__":
    global fd
    fd = open('/tmp/urls.txt', 'w')

    global db
    db = tornado.database.Connection("127.0.0.1", "junk", user='root')

    import tornado.options
    #tornado.options.parse_config_file("/etc/server.conf")
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
