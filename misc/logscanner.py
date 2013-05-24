#!/usr/bin/env python
import sys
import re
import libinjection
import urllib
import urlparse

logre = re.compile(r' /diagnostics\?([^ ]+) HTTP')

def doline(logline):
    """
    ...GET /diagnostics?id=%22union+select HTTP/1.1
    """
    mo = logre.search(logline)
    if not mo:
        return

    sqli= False
    fp = None
    extra = {}
    for key,val in urlparse.parse_qsl(mo.group(1)):
        val = urllib.unquote(val)
        argsqli = libinjection.detectsqli(val, extra)
        if argsqli:
            fp = extra['fingerprint']
        sqli = sqli or argsqli
    if not sqli:
        print "\n---"
        print mo.group(1)
        for key,val in urlparse.parse_qsl(mo.group(1)):
            val = urllib.unquote(val)
            argsqli = libinjection.detectsqli(val, extra)
            print extra['fingerprint'], key+'=', val.strip()


if __name__ == '__main__':
    for line in sys.stdin:
        doline(line)
