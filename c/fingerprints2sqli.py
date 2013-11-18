#!/usr/bin/env python
"""
Small script to convert fingerprints back to SQL or SQLi
"""
import subprocess


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
    mode = 'print'
    fingerprints = []
    with open('fingerprints.txt', 'r') as fd:
        for line in fd:
            fingerprints.append(line.strip())

    for fingerprint in fingerprints:
        sql = []
        for ch in fingerprint:
            sql.append(RMAP[ch])

        sqlstr =  ' '.join(sql)
        if mode == 'print':
            print fingerprint, ' '.join(sql)
        else:
            args = ['./fptool', '-0', sqlstr]
            actualfp = subprocess.check_output(args).strip()
            if fingerprint != actualfp:
                print fingerprint, actualfp, ' '.join(sql)


