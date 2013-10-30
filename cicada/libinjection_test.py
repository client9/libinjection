from QueueAWS import QueueAWS
from StateDynamo import StateDynamo
from events import *
from sourcecontrol import *
from shell import *
from publishers import *

WORKDIR=os.path.expanduser("/var/cicada/workspace")
PUBDIR=os.path.expanduser("/var/cicada/artifacts")

REGION='us-west-2'
QUEUE_EVENT = QueueAWS('cicada_events', REGION)
QUEUE_WORK = QueueAWS('cicada_work', REGION)
DYNAMO =  StateDynamo(REGION)

LISTEN = [
    TestOnEvent('libinjection'),
    TestOnTime(minute='0', hour='23')
]

POLLERS = {
    'poll-git-openssl': {
        'listen': [
            TestOnTime(minute='5', hour='1'),
        ],
        'exec': PollGit('openssl',
                        'git://git.openssl.org/openssl.git',
                        DYNAMO, QUEUE_EVENT)
    },
    'poll-git-modsecurity': {
        'listen': [
            TestOnTime(minute='1', hour='2'),
        ],
        'exec': PollGit('modsecurity',
                        'https://github.com/SpiderLabs/ModSecurity.git',
                        DYNAMO, QUEUE_EVENT)
    },
    'poll-git-ironbee': {
        'listen': [
            TestOnTime(minute='1', hour='2'),
        ],
        'exec': PollGit('ironbee',
                        'https://github.com/ironbee/ironbee',
                        DYNAMO, QUEUE_EVENT)
    },
    'poll-svn-stringencoders': {
        'listen': [
            TestOnInterval(minutes=10),
        ],
        'exec': PollSVN('stringencoders',
                        'http://stringencoders.googlecode.com/svn/trunk/',
                        DYNAMO, QUEUE_EVENT)
    }
}

LISTEN = [
    TestOnEvent('libinjection'),
    TestOnTime(minute='0', hour='23'),
]

OPENSSL = {
    'build-test': {
        'listen': [ TestOnEvent('openssl') ],
        'source': CheckoutGit('git://git.openssl.org/openssl.git', 'openssl'),
        'exec': ExecuteShell("""
cd openssl
./config --no-shared
make
make test
"""),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    }
}

STRINGENCODERS = {
    'stringencoders-test': {
        'listen': [ TestOnEvent('stringencoders') ],
        'source': CheckoutSVN('http://stringencoders.googlecode.com/svn/trunk/', 'stringencoders'),
        'exec': ExecuteShell('cd stringencoders && ./bootstrap.sh && ./configure && make && make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'codecoverage': {
        'listen': [ TestOnEvent('stringencoders') ],
        'source': CheckoutSVN('http://stringencoders.googlecode.com/svn/trunk/', 'stringencoders'),
        'exec': ExecuteShell('cd stringencoders && ./bootstrap.sh && ./configure --enable-gcov && make clean && make lcov-html'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
            PublishArtifact('stringencoders/lcov-html/html', PUBDIR, 'html/src/index.html', 'coverage')
        ]
    }
}

LIBINJECTION = {
    'libinjection-build-test': {
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'    : ExecuteShell('gcc --version && cd libinjection/c && make clean && make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-build-test-g++': {
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('g++ --version && cd libinjection/c && make clean && CC=g++ make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-build-test-clang': {
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('clang --version && cd libinjection/c && ./clang.sh'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-cppcheck': {
        'listen' : LISTEN,
        'source' : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'   : ExecuteShell('cppcheck --version && cd libinjection/c && make cppcheck'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-clang-static-analyzer': {
        'listen' : LISTEN,
        'source' : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'   : ExecuteShell('cd libinjection/c && ./clang-static-analyzer.sh'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-loc': {
        'listen' : LISTEN,
        'source' : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'   : ExecuteShell('cd libinjection/c && cloc.pl libinjection.h libinjection_sqli.c'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-pyflakes': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('cd libinjection/c && pyflakes *.py'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-pylint': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        # disable 'too-many-lines' warning
        'exec': ExecuteShell('pylint --disable=C0302 --include-ids=y -f parseable libinjection/c/*.py'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-python-build-test': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('cd libinjection && make clean && cd python && make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-php-build-test': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('cd libinjection && make clean && cd php && make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-lua-build-test': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec': ExecuteShell('cd libinjection && make clean && cd lua && make test'),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-samples-positive': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'   : ExecuteShell("""
cd libinjection/c
make clean
make reader
./reader -t -i -m 21 ../data/sqli-*.txt
"""),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-samples-negative': {
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'   : ExecuteShell("""
cd libinjection/c
make clean
make reader
./reader -t -m 22 ../data/false_positives.txt
"""),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-coverage-unittest': {
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'    : ExecuteShell("cd libinjection/c && make clean && make coverage-testdriver"),
        'publish' : [
            # 1. file relative to workspace  for PublishConsole, it's empty
            # 2. link url
            # 2. linktext
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
            PublishArtifact('libinjection/c/lcov-html', PUBDIR, 'lcov-html/c/libinjection_sqli.c.gcov.html', 'coverage')
            ]
    },
    'libinjection-speed': {
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec' : ExecuteShell("cd libinjection/c && make test_speed"),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-valgrind': {
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec' : ExecuteShell("cd libinjection/c && make clean && nice make valgrind"),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    },
    'libinjection-gprof': {
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git', 'libinjection'),
        'exec'    : ExecuteShell("""#!/bin/bash
cd libinjection/c
make clean
make reader
gcc -g -O2 -pg -o reader libinjection_sqli.c reader.c
./reader -s -q ../data/sqli-*.txt ../data/false-*.txt
gprof ./reader gmon.out
"""),
        'publish': [
            PublishArtifact('console.txt', PUBDIR, 'console.txt', 'console'),
        ]
    }
}

PROJECTS = {
    'pollers': POLLERS,
    'libinjection': LIBINJECTION,
    'stringencoders': STRINGENCODERS,
    'openssl': OPENSSL
}
