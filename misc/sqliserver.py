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

def print_token_string(tok):
    """
    returns the value of token, handling opening and closing quote characters
    """
    out = ''
    if tok.str_open != libinjection.CHAR_NULL:
        out += tok.str_open
    out += tok.val
    if tok.str_close != libinjection.CHAR_NULL:
        out += tok.str_close
    return out

def print_token(tok):
    """
    prints a token for use in unit testing
    """
    out = ''
    if tok.type == 's':
        out += print_token_string(tok)
    elif tok.type == 'v':
        # SWIG: var_count is still a char, so need to convert back to int
        vc = ord(tok.var_count);
        if vc == 1:
            out += '@'
        elif vc == 2:
            out += '@@'
        out += print_token_string(tok)
    else:
        out += tok.val
    return (tok.type, out)

def alltokens(val, context, comments):

    if context == libinjection.CHAR_NULL:
        contextstr = 'no'
    elif context == libinjection.CHAR_SINGLE:
        contextstr = 'single'
    elif context == libinjection.CHAR_DOUBLE:
        contextstr = 'double'
    else:
        raise RuntimeException("bad quote context")

    if comments == libinjection.COMMENTS_ANSI:
        commentstr = 'ansi'
    elif comments == libinjection.COMMENTS_MYSQL:
        commentstr = 'mysql'
    else:
        raise RuntimeException("bad quote context")

    parse = {
        'comment': commentstr,
        'quote': contextstr
    }
    args = []
    sqlstate = libinjection.sfilter()
    atoken = libinjection.stoken_t()
    libinjection.sqli_init(sqlstate, val, context, comments)
    count = 0
    while count < 25:
        count += 1
        ok = libinjection.sqli_tokenize(sqlstate, atoken)
        if ok == 0:
            break
        args.append(print_token(atoken))


    parse['tokens'] = args

    args = []
    issqli = libinjection.sqli_fingerprint(sqlstate, val, context, comments)
    vec = sqlstate.tokenvec
    for i in range(len(sqlstate.pat)):
        args.append(print_token(vec[i]))
    parse['folds'] = args
    parse['sqli'] = bool(issqli)

    # todo add stats

    return parse

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
        arg = self.request.arguments.get('type', [])
        if len(arg) > 0 and arg[0] == 'tokens':
            return self.get_tokens()
        else:
            return self.get_fingerprints()

    def get_tokens(self):
        ids = self.request.arguments.get('id', [])

        if len(ids) == 1:
            formvalue = ids[0]
        else:
            formvalue = ''

        val = urllib.unquote(formvalue)
        parsed = []
        parsed.append(alltokens(val, libinjection.CHAR_NULL,   libinjection.COMMENTS_ANSI))
        parsed.append(alltokens(val, libinjection.CHAR_NULL,   libinjection.COMMENTS_MYSQL))
        parsed.append(alltokens(val, libinjection.CHAR_SINGLE, libinjection.COMMENTS_ANSI))
        parsed.append(alltokens(val, libinjection.CHAR_SINGLE, libinjection.COMMENTS_MYSQL))
        parsed.append(alltokens(val, libinjection.CHAR_DOUBLE, libinjection.COMMENTS_MYSQL))

        self.render("tokens.html",
                    title='libjection sqli token parsing diagnositcs',
                    version = libinjection.LIBINJECTION_VERSION,
                    parsed=parsed,
                    formvalue=val
                    )

    def get_fingerprints(self):
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
            if name == 'type':
                continue

            fps = []

            val = values[0]
            val = urllib.unquote(val)
            if len(val) == 0:
                continue

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
            if name == 'type':
                continue
            for val in values:
                # do it one more time include cut-n-paste was already url-encoded
                val = urllib.unquote(val)
                if len(val) == 0:
                    continue

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

