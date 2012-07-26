#!/usr/bin/env python
#  Copyright 2012, Nick Galbreath
#  nickg@client9.com
#  GPL v2 License -- Commericial Licenses available.
#  http://www.gnu.org/licenses/gpl-2.0.txt
#
import unittest
from sqlparse_map import sqlipat
from sqlparse import Attacker, constant_folding2, sql_syntax
from urllib import unquote_plus, unquote, quote_plus, quote
from collections import Counter

class AttackTest:
    def __init__(self):
        self.at = Attacker()
        self.stats = {
            'type1': Counter(),
            'type2': Counter(),
            'type3': Counter(),
            'pat': Counter(),
            'pat5': Counter(),
            'failed': Counter(),
            }
        self.sqli = 0
        self.benign = 0

    def dumpStats(self):
        print '----'
        for t in ('pat5',):
            for m in self.stats[t]:
                print t, m, self.stats[t][m]

        print '----'
        for p in sqlipat:
            if p not in self.stats['pat5']:
                print "Unused: " + p
        print '----'
        total = self.sqli + self.benign
        print "SQLI  : %d" % (self.sqli,)
        print "SAFE  : %d" % (self.benign,)
        print "TOTAL : %d" % (total,)


    def testFromFile(self, filename):
        with open(filename, 'r') as fd:
            linenum = 0
            for line in fd:
                linenum += 1
                line = line.strip()
                if len(line) > 0 and line[0] != '#':
                    self.isAttack(filename, linenum, line.strip())

    def isAttack(self, filename, linenum, s):
        s = self.at.qsv_normalize(unquote_plus(s).upper())
        attack = self.at.test(s)
        if attack is not None:
            self.sqli += 1
            self.stats[attack[0]][attack[1]] += 1
            pat5 = attack[2][0:5]
            self.stats['pat5'][pat5]+=1
            s = s.replace("\n", "\\n")
            print("%s:%s %s-%s %s\t%s" % (filename, linenum, attack[0],len(attack[3]),attack[2],s,))
            return True
        else:
            self.benign += 1
            self.stats['failed']
            if '"' in s:
                prefix = '"'
            elif "'" in s:
                prefix = "'"
            else:
                prefix = ''

            tokens = list(constant_folding2(sql_syntax(self.at.lex.tokenize(s, prefix))))
            #tokens = list(sql_syntax(self.at.lex.tokenize(s, prefix)))
            pat = ''.join([ t[0] for t in tokens])
            print "%s:%s False\t %s\t%s"  % (filename, linenum, pat, s)
            return False

if __name__ == '__main__':
    import sys
    import glob
    at = AttackTest()

    if len(sys.argv) == 1:
        files = glob.glob('urls-*.txt')
    else:
        files = sys.argv[1:]

    for f in files:
        at.testFromFile(f)

    at.dumpStats()
