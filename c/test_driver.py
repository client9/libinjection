#!/usr/bin/env python
"""
Test driver
Runs off plain text files similar to how PHP's test harness works
"""
import subprocess

def run(args):
    """
    Runs a command and returns stdout output, throws exception on failed run.
    Uses python's 2.7 check_output if available otherwise uses something else
    """

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
        aprocess = subprocess.Popen(args,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        (stdoutdata, stderrdata) = aprocess.communicate()
        if aprocess.returncode != 0:
            raise Exception("Test died!: " + stderrdata)
        return stdoutdata

def run_test(test_name, data, valgrind=False):
    """
    runs a test
    """

    if valgrind:
        args = ['valgrind', '--gen-suppressions=no', '--read-var-info=yes',
                '--leak-check=full', '--error-exitcode=1',
                '--track-origins=yes', './sqli', data[1]]
        actual = run(args)
    else:
        actual = run(['./sqli', data[1]])

    if actual.strip() != data[2].strip():
        print "not ok: " + test_name
        print "EXPECTED: \n" + data[2]
        print "GOT: \n" + actual
    else:
        print "ok: " + test_name

def read_test(arg):
    """
    Read a test file and split into components
    """

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
    FLAG_VALGRIND = False
    if 'valgrind' in sys.argv[1]:
        i = 2
        FLAG_VALGRIND = True

    for name in sys.argv[i:]:
        print name
        testdata = read_test(name)
        run_test(name, testdata, FLAG_VALGRIND)
        print '----------------'

