#!/usr/bin/env python

import sys

class PermuteFingerprints(object):
    def __init__(self):
        self.fingerprints = set()
        self.blacklist = set([
            'E1n', 'sns', '1&n', 's1s', '1n1', '1o1', '1os', 'sn1',
            'sonc', 'so1', 'n&n', 'son','nov', 'n&s','E1s', 'nos',
            'nkn&n', '1sn', 'n&nkn', 's1n', 'n&nEn', 's&sn', '1os1o',
            'sU', 'nU', 'n,(n)', 'n&n&n', 'Enkn', 'nk1;',
            '1os1o', '1n1;', 's*1s', '1s1', 'nknEn', 'n&sn',
            'so1', 'nkn;', 'n&n;', 'von', 'n&nc',
            'n)o1','Enn;', 'nBn', 'Ennc', 'n&En'
            ])

    def aslist(self):
        return sorted(list(self.fingerprints))

    def insert(self,s):
        if len(s) > 5:
            s = s[0:5]
        if self.validate(s):
            self.fingerprints.add(s)

    def validate(self, s):
        if s == 's&1s':
            # special case of magic ending quote in php
            return True

        if len(s) == 0:
            return False

        if s in self.blacklist:
            return False

        # only 1 special case for this
        # 1;foo:goto foo
        # 1;n:k
        # the 'foo' can only be a 'n' type
        if ':' in s and not 'n:' in s:
            return False

        if '11' in s:
            return False

        if 'v1' in s:
            return False

        if 'nv' in s:
            return False

        # select @version foo is legit
        # but unlikely anywhere else
        if 'vn' in s and 'Evn' not in s:
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

        if 'ff' in s:
            return False

        if 'kno' in s:
            return False

        if 'nEk' in s:
            return False

        if 'n(n' in s:
            return False
        if '1so' in s:
            return False
        if '1s1' in s:
            return False
        if 'noo' in s:
            return False
        if 'ooo' in s:
            return False

        if 'vvv' in s:
            return False

        if 'vsn' in s:
            return False
        if '1vn' in s:
            return False
        if '1n1' in s:
            return False
        if '&1n' in s:
            return False
        if '&1v' in s:
            return False
        if '&1s' in s:
            return False
        if 'nnk' in s:
            return False

        # folded away
        if s.startswith('('):
            return False

        if '&o' in s:
            return False

        if '1,1' in s:
            return False
        if '1,s' in s:
            return False
        if '1,n' in s:
            return False
        if 's,1' in s:
            return False
        if 's,s' in s:
            return False
        if 's,n' in s:
            return False
        if 'n,1' in s:
            return False
        if 'n,s' in s:
            return False
        if 'n,n' in s:
            return False
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
                self.insert(fp[0:i] + 'n'    + fp[i+1:])
                self.insert(fp[0:i] + 'v'    + fp[i+1:])
                self.insert(fp[0:i] + 's'    + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + 'f()'  + fp[i+1:])
                self.insert(fp[0:i] + '1os'  + fp[i+1:])
                self.insert(fp[0:i] + '1ov'  + fp[i+1:])
                self.insert(fp[0:i] + '1on'  + fp[i+1:])
                self.insert(fp[0:i] + '(1)'  + fp[i+1:])
            elif fp[i] == 's':
                self.insert(fp[0:i] + 'v'    + fp[i+1:])
                self.insert(fp[0:i] + '1'    + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + 'f()'  + fp[i+1:])
                self.insert(fp[0:i] + 'so1'  + fp[i+1:])
                self.insert(fp[0:i] + 'sov'  + fp[i+1:])
                self.insert(fp[0:i] + 'son'  + fp[i+1:])
                self.insert(fp[0:i] + '(s)'  + fp[i+1:])
            elif fp[i] == 'v':
                self.insert(fp[0:i] + 's'    + fp[i+1:])
                self.insert(fp[0:i] + '1'    + fp[i+1:])
                self.insert(fp[0:i] + 'f(1)' + fp[i+1:])
                self.insert(fp[0:i] + 'f()'  + fp[i+1:])
                self.insert(fp[0:i] + 'vo1'  + fp[i+1:])
                self.insert(fp[0:i] + 'vos'  + fp[i+1:])
                self.insert(fp[0:i] + 'von'  + fp[i+1:])
                self.insert(fp[0:i] + '(v)'  + fp[i+1:])
            elif fp[i] == 'E':
                # Select top, select distinct, case when
                self.insert(fp[0:i] + 'Ek'   + fp[i+1:])
            elif fp[i] == ')':
                self.insert(fp[0:i] + '))'   + fp[i+1:])
                self.insert(fp[0:i] + ')))'  + fp[i+1:])
                self.insert(fp[0:i] + '))))' + fp[i+1:])

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


