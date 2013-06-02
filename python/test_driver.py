#!/usr/bin/env python
"""
Test driver
Runs off plain text files, similar to how PHP's test harness works
"""
import os
import glob
from libinjection import *

print LIBINJECTION_VERSION

def print_token_string(tok):
    out = ''
    if tok.str_open != CHAR_NULL:
        out += tok.str_open
    out += tok.val
    if tok.str_close != CHAR_NULL:
        out += tok.str_close
    return out

def print_token(tok):
    out = ''
    out += tok.type
    out += ' '
    if tok.type == 's':
        out += print_token_string(tok)
    elif tok.type == 'v':
        vc = ord(tok.var_count);
        if vc == 1:
            out += '@'
        elif vc == 2:
            out += '@@'
        out += print_token_string(tok)
    else:
        out += tok.val
    return out

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

def runtest(testname, flag=None):
    """
    runs a test, optionally with valgrind
    """
    data =  readtestdata(os.path.join('../tests', testname))

    sql_state = sfilter()
    actual = ''

    if flag == 'tokens':
        atoken = stoken_t()
        sqli_init(sql_state, data[1], CHAR_NULL, COMMENTS_ANSI);
        while sqli_tokenize(sql_state, atoken):
            actual += print_token(atoken) + '\n';
        actual = actual.strip()
    elif flag == 'folding':
        sqli_fingerprint(sql_state, data[1], CHAR_NULL, COMMENTS_ANSI);
        for i in range(len(sql_state.pat)):
            actual += print_token(sql_state.tokenvec[i]) + '\n';
    elif flag == 'fingerprints':
        ok = is_sqli(sql_state, data[1], None)
        if ok:
            actual = sql_state.pat
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

def run_tokens(testname):
    runtest(testname, 'tokens')

def run_folding(testname):
    runtest(testname, 'folding')

def run_fingerprints(testname):
    runtest(testname, 'fingerprints')

def test_tokens():
    for testname in sorted(glob.glob('../tests/test-tokens-*.txt')):
        testname = os.path.basename(testname)
        yield run_tokens, testname


def test_folding():
    for testname in sorted(glob.glob('../tests/test-folding-*.txt')):
        testname = os.path.basename(testname)
        yield run_folding, testname

def test_fingerprints():
    for testname in sorted(glob.glob('../tests/test-sqli-*.txt')):
        testname = os.path.basename(testname)
        yield run_fingerprints, testname

if __name__ == '__main__':
    import sys
    sys.stderr.write("run using nosetests\n")
    sys.exit(1)
