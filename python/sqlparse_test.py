#!/usr/bin/env python
import unittest
from sqlparse_exploits import Attacker
import urllib

from sqlparse import SQLexer

class TestSequenceFunctions(unittest.TestCase):
    def testParser(self):
        s = SQLexer()

        tokens = s.tokenize('1 "foo" "bar" 1')
        self.assertEquals( [('1', '1'), ('s', '"foo"'), ('s', '"bar"'), ('1', '1')], tokens )
        tokens = s.syntax(tokens)
        self.assertEquals( [('1', '1'), ('s', '"foo""bar"'), ('1', '1')], tokens)

        tokens = s.tokenize('"foo" "bar" 1')
        self.assertEquals( [('s', '"foo"'), ('s', '"bar"'), ('1','1')], tokens )
        tokens = s.syntax(tokens)
        self.assertEquals( [('s', '"foo""bar"'),('1', '1')], tokens)

        tokens = s.tokenize('1 "foo" "bar" 1')
        self.assertEquals( [('1','1'), ('s', '"foo"'), ('s', '"bar"'), ('1','1')], tokens )
        tokens = s.syntax(tokens)
        self.assertEquals( [('1', '1'), ('s', '"foo""bar"'), ('1', '1') ], tokens)


        tokens = s.tokenize('select 1'.upper())
        self.assertEquals( [('k', 'SELECT'), ('1', '1')], tokens)

        tokens = s.tokenize('1 /* foo */ 2'.upper())
        self.assertEquals( [('1', '1'), ('c', '/* FOO */'), ('1', '2')], tokens)

        tokens = s.tokenize('1 /*foo*/ 2'.upper())
        self.assertEquals( [('1', '1'), ('c', '/*FOO*/'), ('1', '2')], tokens)

        tokens = s.tokenize('1 /*foo*/ 2'.upper())
        self.assertEquals( [('1', '1'), ('c', '/*FOO*/'), ('1', '2')], tokens)

        tokens = s.tokenize('1 || select'.upper())
        self.assertEquals( [('1', '1'), ('o', '||'), ('k', 'SELECT')], tokens)

        tokens = s.tokenize('1 /*! || */ select'.upper())
        self.assertEquals( [('1', '1'), ('o', '||'), ('k', 'SELECT')], tokens)

        tokens = s.tokenize('1 /*!32302 || */ select'.upper())
        self.assertEquals( [('1', '1'), ('o', '||'), ('k', 'SELECT')], tokens)

        tokens  = s.tokenize('select 1 /*!00000AND 2>1*/'.upper());
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), ('o', 'AND'), ('1', '2'), ('o', '>'), ('1', '1')], tokens)

        tokens = s.tokenize('@@NEW UNION#SQLMAP'.upper())
        self.assertEquals( [('v', '@@NEW'), ('o', 'UNION'), ('c', '#SQLMAP')], tokens)

        #tokens = s.tokenize('"FOO" IN BOOLEAN MODE'.upper())
        #self.assertEquals( [('string', 'FOO'), ('k', 'IN BOOLEAN MODE')], tokens)

        # mysql comments terminate on normal "*/" AND
        # on another C-style start comment /*  !!!!

        # ==> select 1,2
        tokens = s.tokenize("SELECT /*!000001,/*!000002")
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), (',', ','), ('1', '2')], tokens)

        tokens = s.tokenize("SELECT /*!1,/*!2*/")
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), (',', ','), ('1', '2')], tokens)

        # ==> select 1,2
        tokens = s.tokenize("SELECT /*!000001,/*!000002*/")
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), (',', ','), ('1', '2')], tokens)

        # ==> select 1,2,3
        tokens = s.tokenize("SELECT /*!000001,/*!2*/,3")
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), (',', ','), ('1', '2'), (',', ','), ('1', '3')], tokens)

        # ==> select 1,2,3
        tokens = s.tokenize("SELECT /*!000001,/*!2*/,3")
        self.assertEquals( [('k', 'SELECT'), ('1', '1'), (',', ','), ('1', '2'), (',', ','), ('1', '3')], tokens)

        tokens = s.tokenize("1+2")
        self.assertEquals( [('1', '1'), ('o', '+'), ('1','2')], tokens)

        tokens = s.tokenize("1 /**/UNION/**/SELECT")
        self.assertEquals( [('1', '1'), ('c', '/**/'), ('o', 'UNION'), ('c', '/**/'), ('k', 'SELECT')], tokens)
        tokens = s.syntax(tokens)
        self.assertEquals( [('1', '1'), ('o', 'UNION'), ('k', 'SELECT')], tokens)

        tokens = s.tokenize("1 /**/UNION/**/ALL/**/SELECT")
        #self.assertEquals( [('1', '1'), ('c', '/**/'), ('o', 'UNION'), ('c', '/**/'), ('k', 'SELECT')], tokens)
        tokens = s.syntax(tokens)
        self.assertEquals( [('1', '1'), ('o', 'UNION ALL'), ('k', 'SELECT')], tokens)



    def testConstantFolding(self):
        at = Attacker()
        sample = ( ('1', '9'), ('o', '-'), ('1', '2'), ('o', '-'), ('1', '5'))
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '9')], tokens)

        sample = ( ('string', '9'), ('o', '-'), ('string', '2'), ('o', '-'), ('string', '5'))
        tokens = at.constant_folding2(sample)
        self.assertEquals( list(sample), tokens)

        #sample = ( ('string', 'STAR'), ('o', 'AND'), ('n', 'WARS'), ('o', '-'), ('1', '345.345'))
        #tokens = at.constant_folding(sample)
        #self.assertEquals( [('string', 'STAR')], tokens)


        sample = ( ('o', '-'), ('1', '9'), ('o', '-'), ('1', '2'), ('o', '-'), ('1', '5'))
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '9')], tokens)

        sample = ( ('1', '12'), ('o', '/'), ('1', '12'), ('o', '/'), ('1', '2012'))
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '12')], tokens)

        sample = [ ('1', '1') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '1')], tokens)

        sample = [ ('1', '12') , ('n', 'foo')]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '12'), ('n', 'foo')], tokens)

        sample = [ ('1', '1'), ('L', '(') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '1'), ('L', '(')], tokens)

        sample = [ ('1', '12'), ('o', '+') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '12'), ('o', '+')], tokens)

        sample = [ ('1', '12'), ('o', '+'), ('L', '(') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '12'), ('o', '+'), ('L', '(') ], tokens)

        sample = [ ('1', '12'), ('o', '+'), ('f', 'PI'), ('L', '(') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('1', '12'), ('o', '+'), ('f', 'PI'), ('L', '(') ], tokens)


        sample = [ ('n', 'X'), ('o', '+'), ('n', 'Y') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( sample, tokens)

        sample = [ ('n', 'X'), ('o', '+'), ('1', '1') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( sample, tokens)

        sample = [ ('n', 'X'), ('o', '+'), ('o', '-'), ('o', '+'), ('1', '1') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('n', 'X'), ('o', '+'), ('1', '1')], tokens)

        sample = [ ('n', 'X'), ('o', '+'), ('o', '-'),('1', '1') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('n', 'X'), ('o', '+'), ('1', '1')], tokens)

        sample = [ ('n', 'X'), ('o', '/'), ('n', 'Y'), ('o', '/') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [('n', 'X'), ('o', '/'), ('n', 'Y'), ('o', '/')], tokens)

        sample = [ ('s', '"X"'), ('o', '+'), ('o', '-'), ('1', '4') ]
        tokens = at.constant_folding2(sample)
        self.assertEquals( [ ('s', '"X"'), ('o', '+'), ('1', '4') ], tokens)


if __name__ == '__main__':
    unittest.main()
