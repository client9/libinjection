#!/usr/bin/env python
"""
Test driver
Runs off plain text files, similar to how PHP's test harness works
"""
import os
import glob
from libinjection import *
from words import *

print LIBINJECTION_VERSION

def print_token_string(tok):
    """
    returns the value of token, handling opening and closing quote characters
    """
    out = ''
    if tok.str_open != "\0":
        out += tok.str_open
    out += tok.val
    if tok.str_close != "\0":
        out += tok.str_close
    return out

def print_token(tok):
    """
    prints a token for use in unit testing
    """
    out = ''
    out += tok.type
    out += ' '
    if tok.type == 's':
        out += print_token_string(tok)
    elif tok.type == 'v':
        vc = tok.count;
        if vc == 1:
            out += '@'
        elif vc == 2:
            out += '@@'
        out += print_token_string(tok)
    else:
        out += tok.val
    return out.strip()

def toascii(data):
    """
    Converts a utf-8 string to ascii.   needed since nosetests xunit is not UTF-8 safe
    https://github.com/nose-devs/nose/issues/649
    https://github.com/nose-devs/nose/issues/692
    """
    udata = data.decode('utf-8')
    return udata.encode('ascii', 'xmlcharrefreplace')

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

    return (info['--TEST--'], info['--INPUT--'].strip(), info['--EXPECTED--'].strip())

def runtest(testname, flag, sqli_flags):
    """
    runs a test, optionally with valgrind
    """
    data =  readtestdata(os.path.join('../tests', testname))

    sql_state = sqli_state()
    sqli_init(sql_state, data[1], sqli_flags)
    sqli_callback(sql_state, lookup)
    actual = ''

    if flag == 'tokens':
        while sqli_tokenize(sql_state):
            actual += print_token(sql_state.current) + '\n';
        actual = actual.strip()
    elif flag == 'folding':
        sqli_fingerprint(sql_state, sqli_flags)
        for i in range(len(sql_state.fingerprint)):
            actual += print_token(sqli_get_token(sql_state, i)) + '\n';
    elif flag == 'fingerprints':
        ok = is_sqli(sql_state)
        if ok:
            actual = sql_state.fingerprint
    else:
        raise RuntimeException("unknown flag")

    actual = actual.strip()

    if actual != data[2]:
        print "INPUT: \n" + toascii(data[1])
        print
        print "EXPECTED: \n" + toascii(data[2])
        print
        print "GOT: \n" + toascii(actual)
        assert actual == data[2]

def test_tokens():
    def run_tokens(testname):
        runtest(testname, 'tokens', libinjection.FLAG_QUOTE_NONE | libinjection.FLAG_SQL_ANSI)

    for testname in sorted(glob.glob('../tests/test-tokens-*.txt')):
        testname = os.path.basename(testname)
        yield run_tokens, testname

def test_tokens_mysql():
    def run_tokens(testname):
        runtest(testname, 'tokens', libinjection.FLAG_QUOTE_NONE | libinjection.FLAG_SQL_MYSQL)

    for testname in sorted(glob.glob('../tests/test-tokens_mysql-*.txt')):
        testname = os.path.basename(testname)
        yield run_tokens, testname

def test_folding():
    def run_folding(testname):
        runtest(testname, 'folding', libinjection.FLAG_QUOTE_NONE | libinjection.FLAG_SQL_ANSI)

    for testname in sorted(glob.glob('../tests/test-folding-*.txt')):
        testname = os.path.basename(testname)
        yield run_folding, testname

def test_fingerprints():
    def run_fingerprints(testname):
        runtest(testname, 'fingerprints', 0)


    for testname in sorted(glob.glob('../tests/test-sqli-*.txt')):
        testname = os.path.basename(testname)
        yield run_fingerprints, testname

if __name__ == '__main__':
    import sys
    sys.stderr.write("run using nosetests\n")
    sys.exit(1)
