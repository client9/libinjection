#!/usr/bin/env python

from subprocess import check_output

def run_test(name, data):
    actual = check_output(['./sqli', data[1]])
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

    return (info['--TEST--'],info['--INPUT--'],info['--EXPECTED--'])

if __name__ == '__main__':
    import sys
    for name in sys.argv[1:]:
        testdata = read_test(name)
        run_test(name, testdata)


