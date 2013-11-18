#!/usr/bin/env python

"""
Small script to convert fingerprints back to
SQL or SQLi
"""

RMAP = {
    '1': '1',
    'f': '',
    '&': 'and',
    'v': '@version',
    'n': 'aname',
    's': "\"1\"",
    '(': '(',
    ')': ')',
    'o': '-',
    'E': 'select',
    'U': 'union',
    'k': "KEYWORD",
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
        print fingerprint, ' '.join(sql)

