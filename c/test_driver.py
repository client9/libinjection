#!/usr/bin/env python

import subprocess

def run(args):

    try:
        getattr(subprocess, 'check_output')
        has_check_output = True
    except AttributeError:
        has_check_output = False

    if has_check_output:
        # 2.7
        return subprocess.check_output(args)
    else:
        # not 2.7
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = p.communicate()
        if p.returncode != 0:
            raise Exception("Test died!: " + stderrdata)
        return stdoutdata

def run_test(name, data, valgrind=False):
    if valgrind:
        args = ['valgrind', '--gen-suppressions=no', '--read-var-info=yes',
                '--leak-check=full', '--error-exitcode=1',
                '--track-origins=yes', './sqli', data[1]]
        actual = run(args)
    else:
        actual = run(['./sqli', data[1]])

    if actual.strip() != data[2].strip():
        print "not ok: " + name
        print "EXPECTED: \n" + data[2]
        print "GOT: \n" + actual
    else:
        print "ok: " + name

def read_test(arg):
    fd = open(arg, 'r')
    state = None
    info = {
        '--TEST--': '',
        '--INPUT--': '',
        '--EXPECTED--': ''
        }

    for line in fd:
        line = line.rstrip()
        if line in ('--TEST--', '--INPUT--', '--EXPECTED--'):
            state = line
        elif state:
            info[state] += line + '\n'

    # remove last newline from input
    info['--INPUT--'] = info['--INPUT--'][0:-1]

    return (info['--TEST--'], info['--INPUT--'], info['--EXPECTED--'])

if __name__ == '__main__':
    import sys

    # hack for command line switch
    # if argv1 had 'valgrind'

    i = 1
    valgrind = False
    if 'valgrind' in sys.argv[1]:
        i = 2
        valgrind = True

    for name in sys.argv[i:]:
        print name
        testdata = read_test(name)
        run_test(name, testdata, valgrind)
        print '----------------'

