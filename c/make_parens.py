#!/usr/bin/env python

import sys

class PermuteFingerprints(object):
    def __init__(self):
        self.fingerprints = set()

    def aslist(self):
        return sorted(list(self.fingerprints))

    def insert(self,s):
        if len(s) > 5:
            s = s[0:5]
        if self.validate(s):
            self.fingerprints.add(s)

    def validate(self, s):
        if len(s) == 0:
            return False

        if '11' in s:
            return False

        if 'v1' in s:
            return False

        if 'nv' in s:
            return False

        # all 'ns' in union statements
        if 'U' not in s and 'ns' in s:
            return False

        # select foo (as) bar is only nn type i know
        if 'nn' in s and 'Enn' not in s:
            return False

        if 'kk' in s:
            return False

        if 'ss' in s:
            return False

        if 'ooo' in s:
            return False

        if 'vvv' in s:
            return False

        # folded away
        if '1o1' in s:
            return False
        if '1on' in s:
            return False
        if 'no1' in s:
            return False
        if 'non' in s:
            return False
        if '1(v' in s:
            return False
        if '1(n' in s:
            return False
        if '1(s' in s:
            return False
        if '1(1' in s:
            return False
        if 's(s' in s:
            return False
        if 's(n' in s:
            return False
        if 's(1' in s:
            return False
        if 's(v' in s:
            return False
        if 'v(s' in s:
            return False
        if 'v(n' in s:
            return False
        if 'v(1' in s:
            return False
        if 'v(v' in s:
            return False

        if s.startswith('vs'):
            return False

        if ')(' in s:
            return False

        # need to investigate E(vv) to see
        # if it's correct
        if 'vv' in s and s != 'E(vv)':
            return False

        # bogus
        if s in ('E1n', 'sns', '1&n', 's1s', '1n1', '1o1', '1os'):
            return False

        # unlikely to be sqli but case FP
        if s in ('so1n)', 'sonoE'):
            return False

        return True

    def permute(self, fp):

        self.insert(fp)

        # do this for safety
        if len(fp) > 1 and len(fp) < 5 and fp[-1] != ';' and fp[-1] != 'c':
            self.insert(fp + ";")
            self.insert(fp + ";c")

        # do this for safety
        if len(fp) > 1 and len(fp) < 5 and fp[-1] != 'c':
            self.insert(fp + "c")

        for i in range(len(fp)):
            if fp[i] == '1':
                self.insert(fp[0:i] + 'v' + fp[i+1:])
                self.insert(fp[0:i] + 's' + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + '1os' + fp[1:])
                self.insert(fp[0:i] + '1ov' + fp[1:])
                self.insert(fp[0:i] + '1on' + fp[1:])
            elif fp[i] == 's':
                self.insert(fp[0:i] + 'v' + fp[i+1:])
                self.insert(fp[0:i] + '1' + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + 'so1' + fp[1:])
                self.insert(fp[0:i] + 'sov' + fp[1:])
                self.insert(fp[0:i] + 'son' + fp[1:])
            elif fp[i] == 'v':
                self.insert(fp[0:i] + 's' + fp[i+1:])
                self.insert(fp[0:i] + '1' + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + 'vo1' + fp[1:])
                self.insert(fp[0:i] + 'vos' + fp[1:])
                self.insert(fp[0:i] + 'von' + fp[1:])
            elif fp[i] == ')':
                self.insert(fp[0:i] + '))' + fp[1:])
                self.insert(fp[0:i] + ')))' + fp[1:])
                self.insert(fp[0:i] + '))))' + fp[1:])

        if '(' in fp:

            done = False
            parts = []
            for c in fp:
                if c == '(' and done is False:
                    parts.append(c)
                    done = True
                parts.append(c)
            newline = ''.join(parts)
            self.insert(newline)

            done = False
            parts = []
            for c in fp:
                if c == '(':
                    if done is True:
                        parts.append(c)
                    else:
                        done = True
                parts.append(c)
            newline = ''.join(parts)
            self.insert(newline)

            done = False
            parts = []
            for c in fp:
                if c == '(':
                    parts.append(c)
                parts.append(c)
            newline = ''.join(parts)
            self.insert(newline)


if __name__ == '__main__':
    """
     this "doubles all parathensis"
     to make new fingerprints
     """

    mutator = PermuteFingerprints()

    for line in sys.stdin:
        mutator.permute(line.strip())

    for fp in mutator.aslist():
        print fp


