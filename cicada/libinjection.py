#!/usr/bin/env python
from cicada import *
tests = [
    {
        'name'    : 'libinjection-build-test',
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'    : ExecuteShell('gcc --version && cd c && make clean && make test'),
    },
    {
        'name': 'libinjection-build-test-g++',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('g++ --version && cd c && make clean && CC=g++ make test')
    },
    {
        'name': 'libinjection-pyflakes',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('cd c && pyflakes *.py')
    },
    {
        'name': 'libinjection-pylint',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('pylint --include-ids=y -f parseable c/*.py')
    },
    {
        'name': 'libinjection-python-build-test',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('make clean && cd python && make test'),
    },
    {
        'name': 'libinjection-samples-positive',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'   : ExecuteShell("""
cd c
make clean
make reader
./reader -t -i -m 37 ../data/sqli-*.txt
""")

    },
    {
        'name': 'libinjection-samples-negative',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'   : ExecuteShell("""
cd c
make clean
make reader
./reader -t -m 24 ../data/false_positives.txt
""")
    },
    {
        'name': 'libinjection-coverage-1',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),

    },
    {
        'name'    : 'libinjection-gprof',
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'    : ExecuteShell("make coverage-testdriver")
        'publish' : [
            PublishArtifact('c/lcov-html')
            ]
    },
    {
        'name': 'libinjection-valgrind',
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec' : ExecuteShell("cd c && make clean && nice make valgrind"),
    }
]

import sys
import logging
import os
import os.path

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) == 2:
        workspace = sys.argv[1]
    else:
        workspace = os.path.expanduser("~/libinjection-cicada-workspace")

    pubspace = os.path.join(workspace, "cicada")
    cicada(workspace, pubspace, tests)
