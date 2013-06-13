#!/usr/bin/env python

import json
import sys
from urlparse import *
import urllib
import libinjection

from tornado import template
from tornado.escape import *

def doline(line):

    data = json.loads(line)
    if  not data['request'].startswith("/diagnostics"):
        return None

    urlparts = urlparse(data['request'])
    if len(urlparts.query) == 0:
        return None

    qs = parse_qs(urlparts.query)

    if u'id' not in qs:
        print "no 'id'"
        return None

    # part one, normal decode
    target = urllib.unquote_plus(qs['id'][0])

    # do it again, but preserve '+'
    target = urllib.unquote(target)

    sstate = libinjection.sqli_state()
    libinjection.sqli_init(sstate, target.encode('utf-8'), 0)
    sqli = bool(libinjection.is_sqli(sstate))

    return (target, sqli, sstate.pat)


if __name__ == '__main__':
    s = """
    {"timestamp":1371091563,"remote_ip":"219.110.171.2","request":"/diagnostics?id=1+UNION+ALL+SELECT+1<<<&type=fingerprints","method":"GET","status":200,"user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1","referrer":"https://libinjection.client9.com/diagnostics","duration_usec":160518 }
    """
    fh = [s,]
    fh = open('/var/log/apache2/access-json.log', 'r')

    targets = set()
    table = []
    for line in fh:
        parts = doline(s)
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
                parts[0].replace(',', ', '),
                parts[1],
                parts[2]
                )
            )

    table = reversed(table)

    loader = template.Loader(".")

    txt = loader.load("logtable.html").generate(
        table=table
        )

    print txt



