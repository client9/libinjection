#!/usr/bin/env python
"""
Test driver
Runs off plain text files, similar to how PHP's test harness works
"""
import subprocess
import os
import glob

def toascii(data):
    """
    Converts a utf-8 string to ascii.
    Needed since nosetests xunit is not UTF-8 safe
    https://github.com/nose-devs/nose/issues/649
    https://github.com/nose-devs/nose/issues/692
    """
    udata = data.decode('utf-8')
    return udata.encode('ascii', 'xmlcharrefreplace')

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
        # turn off warning on 2.6 systems
        # pylint: disable=E1101
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

def readtestdata(filename):
    """
    Read a test file and split into components
    """

    state = None
    info = {
        '--TEST--': '',
        '--INPUT--': '',
        '--EXPECTED--': ''
        }

    for line in open(filename, 'r'):
        line = line.rstrip()
        if line in ('--TEST--', '--INPUT--', '--EXPECTED--'):
            state = line
        elif state:
            info[state] += line + '\n'

    # remove last newline from input
    info['--INPUT--'] = info['--INPUT--'][0:-1]

    return (
        info['--TEST--'],
        info['--INPUT--'].strip(),
        info['--EXPECTED--'].strip()
    )

def runtest(testname, flags=None):
    """
    runs a test, optionally with valgrind
    """
    data =  readtestdata(os.path.join('../tests', testname))

    if os.environ.get('VALGRIND', None):
        args = [
            'valgrind',
            '--gen-suppressions=no',
            '--read-var-info=yes',
            '--error-exitcode=1',
            '--track-origins=yes',
            ]
    else:
        args = []

    args.append(os.getenv('PARSER_CMD', './sqli'))

    if flags:
        for flag in flags:
            args.append(flag)

    args.append(data[1])
    actual = run(args)

    actual = actual.strip()

    if actual != data[2]:
        print "INPUT: \n" + toascii(data[1])
        print
        print "EXPECTED: \n" + toascii(data[2])
        print
        print "GOT: \n" + toascii(actual)
        assert actual == data[2]

def run_tokens(testname):
    """ run a single generic SQL token parsing test """
    runtest(testname, [ '-q0', '-ca'])

def run_tokens_mysql(testname):
    """ run a single MySQL token parsing test """
    runtest(testname, [ '-q0', '-cm'])

def run_folding(testname):
    """ run a single folding test """
    runtest(testname, ['-f', '-q0', '-ca'])

def run_sqli(testname):
    """ run a single sqli detection test """
    runtest(testname, ['-d', ])

def test_tokens():
    """ wrapper for generic SQL token parsing """
    for testname in sorted(glob.glob('../tests/test-tokens-*.txt')):
        testname = os.path.basename(testname)
        yield run_tokens, testname

def test_tokens_mysql():
    """ testing for mysql specific parsing """
    for testname in sorted(glob.glob('../tests/test-tokens_mysql-*.txt')):
        testname = os.path.basename(testname)
        yield run_tokens_mysql, testname

def test_folding():
    """ wrapper for testing folding """
    for testname in sorted(glob.glob('../tests/test-folding-*.txt')):
        testname = os.path.basename(testname)
        yield run_folding, testname

def test_sqli():
    """ wrapper for testing high level is_sqli """
    for testname in sorted(glob.glob('../tests/test-sqli-*.txt')):
        testname = os.path.basename(testname)
        yield run_sqli, testname

if __name__ == '__main__':
    import sys
    sys.stderr.write("run using nosetests\n")
    sys.exit(1)
