#!/usr/bin/env python

import datetime
import json
import sys
from urlparse import *
import urllib
import libinjection

from tornado import template
from tornado.escape import *

# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def breakify(s):
    output = ""
    for c in chunks(s, 40):
        output += c
        if ' ' not in c:
            output += ' '
    return output

def doline(line):

    try:
        #line = line.replace("\\x", "%")
        data = json.loads(line)
    except ValueError, e:
        sys.stderr.write("BAD LINE: " + line)
        return None

    if  not data.get('request_uri','').startswith("/diagnostics"):
        return None

    urlparts = urlparse(data['request_uri'])
    if len(urlparts.query) == 0:
        return None

    qs = parse_qs(urlparts.query)

    if u'id' not in qs:
        #print "no 'id'"
        return None

    # part one, normal decode
    target = urllib.unquote_plus(qs['id'][0])

    # do it again, but preserve '+'
    target = urllib.unquote(target)

    sstate = libinjection.sqli_state()
    # BAD the string created by target.encode is stored in
    #   sstate but not reference counted, so it can get
    #   deleted by python
    #    libinjection.sqli_init(sstate, target.encode('utf-8'), 0)

    # instead make a temporary var in python
    # with the same lifetime as sstate (above)
    targetutf8 = target.encode('utf-8')
    libinjection.sqli_init(sstate, targetutf8, 0)

    sqli = bool(libinjection.is_sqli(sstate))

    return (target, sqli, sstate.fingerprint, data['remote_addr'])


if __name__ == '__main__':
    s = """
{"timestamp":1371091563,"remote_ip":"219.110.171.2","request":"/diagnostics?id=1+UNION+ALL+SELECT+1<<<&type=fingerprints","method":"GET","status":200,"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1","referrer":"https://libinjection.client9.com/diagnostics","duration_usec":160518 }
{"timestamp":1371091563,"remote_ip":"219.110.171.2","request":"/diagnostics?id=2+UNION+ALL+SELECT+1<<<&type=fingerprints","method":"GET","status":200,"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1","referrer":"https://libinjection.client9.com/diagnostics","duration_usec":160518 }
"""
    if len(sys.argv) == 1:
        fname = '/var/log/nginx/access.log'
        #fname = '/var/log/apache2/access-json.log'
    else:
        fname = sys.argv[1]

    #fh = s.strip().split("\n")
    fh = open(fname, 'r')

    targets = set()
    table = []
    for line in fh:
        parts = doline(line.strip())
        if parts is None:
            continue

        # help it render in HTML
        if parts[0] in targets:
            continue
        else:
            targets.add(parts[0])

            # add link
            # add form that might render ok in HTML
            # is sqli
            # fingerprint
            table.append( (
                "/diagnostics?id=" + url_escape(parts[0]),
                breakify(parts[0].replace(',', ', ').replace('/*', ' /*')),
                parts[1],
                parts[2],
                parts[3]
                )
            )

    table = reversed(table)

    loader = template.Loader(".")

    txt = loader.load("logtable.html").generate(
        table=table,
        now = str(datetime.datetime.now()),
	ssl_protocol='',
	ssl_cipher=''
        )

    print txt



