#!/usr/bin/env python

import subprocess

"""
Small script to convert fingerprints back to
SQL or SQLi
"""

RMAP = {
    '1': '1',
    'f': 'convert',
    '&': 'and',
    'v': '@version',
    'n': 'aname',
    's': "\"1\"",
    '(': '(',
    ')': ')',
    'o': '*',
    'E': 'select',
    'U': 'union',
    'k': "JOIN",
    't': 'binary',
    ',': ',',
    ';': ';',
    'c': ' -- comment',
    'T': 'DROP',
    ':': ':',
    'A': 'COLLATE',
    'B': 'group by',
    'X': '/* /* nested comment */ */'
}

if __name__ == '__main__':

    fingerprints = []
    with open('fingerprints.txt', 'r') as fd:
        for line in fd:
            fingerprints.append(line.strip())

    for fingerprint in fingerprints:
        sql = []
        for ch in fingerprint:
            sql.append(RMAP[ch])

        sqlstr =  ' '.join(sql)
        if True:
            print fingerprint, ' '.join(sql)
        else:
            actualfp = subprocess.check_output(['./fptool', '-0', sqlstr]).strip()
            if fingerprint != actualfp:
                print fingerprint, actualfp, ' '.join(sql)


