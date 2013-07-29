LISTEN = [
    TestOnEvent('libinjection'),
    TestOnTime(minute='0', hour='23')
]

tests = [
    {
        'name'    : 'libinjection.client9.com-sslassert',
        'listen'  : [  TestOnTime(minute='1') ],
        'source'  : CheckoutGit('https://github.com/client9/sslassert.git'),
        'exec'    : ExecuteShell("OPENSSL=/usr/local/ssl/bin/openssl ./example-libinjection.sh")
    },
    {
        'name'    : 'libinjection-build-test',
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'    : ExecuteShell('gcc --version && cd c && make clean && make test'),
    },
    {
        'name': 'libinjection-build-test-g++',
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('g++ --version && cd c && make clean && CC=g++ make test')
    },
    {
        'name': 'libinjection-pyflakes',
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('cd c && pyflakes *.py')
    },
    {
        'name': 'libinjection-pylint',
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('pylint --include-ids=y -f parseable c/*.py')
    },
    {
        'name': 'libinjection-python-build-test',
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec': ExecuteShell('make clean && cd python && make test'),
    },
    {
        'name': 'libinjection-samples-positive',
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'   : ExecuteShell("""
cd c
make clean
make reader
./reader -t -i -m 24 ../data/sqli-*.txt
""")

    },
    {
        'name': 'libinjection-samples-negative',
        'listen': LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'   : ExecuteShell("""
cd c
make clean
make reader
./reader -t -m 24 ../data/false_positives.txt
""")
    },
    {
        'name'    : 'libinjection-coverage-unittest',
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'    : ExecuteShell("cd c && nice make coverage-testdriver"),
        'publish' : [
            PublishArtifact('c/lcov-html', 'lcov-html/c/libinjection_sqli.c.gcov.html', 'coverage')
            ]
    },
    {
        'name': 'libinjection-speed',
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec' : ExecuteShell("cd c && make test_speed")
    },
    {
        'name': 'libinjection-valgrind',
        'listen'  : LISTEN,
        'source': CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec' : ExecuteShell("cd c && make clean && nice make valgrind"),
    },
    {
        'name'    : 'libinjection-gprof',
        'listen'  : LISTEN,
        'source'  : CheckoutGit('https://github.com/client9/libinjection.git'),
        'exec'    : ExecuteShell("""#!/bin/bash
cd c
make clean
make reader
gcc -g -O2 -pg -o reader libinjection_sqli.c reader.c
./reader -s -q ../data/sqli-*.txt ../data/false-*.txt
gprof ./reader gmon.out
""")
    }
]
