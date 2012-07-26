#!/usr/bin/env python
#  Copyright 2012, Nick Galbreath
#  nickg@client9.com
#  GPL v2 License -- Commericial Licenses available.
#  http://www.gnu.org/licenses/gpl-2.0.txt
#
"""
"""

import re
from urlparse import parse_qsl
from urllib import unquote, unquote_plus

from sqlparse_map import *

def sql_syntax(tokens):

    lasttoken = None
    lastcomment = None

    for thistoken in tokens:
        ttype = thistoken[0]
        tvalue = thistoken[1]

        # skip comments
        if ttype == 'c':
            lastcomment = thistoken
            continue

        lastcomment = None

        # skip strings, keywords, operators
        if ttype == '1' or ttype ==  'f' or ttype == 'v':
            if lasttoken:
                yield lasttoken
                lasttoken = None
            yield thistoken

        elif ttype == 's':
            if lasttoken:
                if lasttoken[0] == 's':
                    lasttoken = ('s', lasttoken[1] + tvalue)
                else:
                    yield lasttoken
                    lasttoken = thistoken
            else:
                lasttoken = thistoken

        # build multi-word operators
        elif ttype == 'o':
            # do we have previous token?
            if lasttoken:
                if lasttoken[0] == 'o' and lasttoken[1] in operator_phrases and thistoken[1] in operator_phrases[lasttoken[1]]:
                    yield ('o', lasttoken[1] + ' ' + thistoken[1])
                    lasttoken = None

                # skip duplicated unary operators
                elif lasttoken[0] == 'o' and lasttoken[1] in ('+', '-', '~', '!'):
                    pass
                else:
                    yield lasttoken
                    lasttoken = thistoken
            elif thistoken[1] in operator_phrases:
                lasttoken = thistoken
            else:
                # hack for case where 'IN' is dual function/keyword
                yield thistoken
                lasttoken = None

            # build muli-word keywords
        else:
            # do we have previous token?
            if lasttoken:
                if lasttoken[1] in keyword_phrases and thistoken[1] in keyword_phrases[lasttoken[1]]:
                    lasttoken = ('k', lasttoken[1] + ' ' + thistoken[1])

                elif lasttoken[1] in operator_phrases and thistoken[1] in operator_phrases[lasttoken[1]]:
                    yield ('o', lasttoken[1] + ' ' + thistoken[1])
                    lasttoken = None
                else:
                    if lasttoken == ('n', 'IN'):
                        lasttoken = ('f', 'IN')
                    yield lasttoken
                    lasttoken = thistoken
            elif thistoken[1] in keyword_phrases:
                lasttoken = thistoken
            else:
                yield thistoken
                lasttoken = None

    if lasttoken:
        yield lasttoken

    # finally
    # the last element is a comment, add that.  This for better identification of SQLi attacks
    if lastcomment:
        yield lastcomment


# simplfies  basic arithmetic expressions tha might be used
# as english abbreviatio
# merges ';;' in to ';'
def constant_folding2(tokens):
    last = None
    first_num = True
    skip_parens = True
    # skip all leading left-parens and unary chars

    for t in tokens:
        #print t, last
        ttype = t[0]

        if skip_parens:
            if ttype == '(' or (ttype == 'o' and t[1] in ('-', '+', '~', '!')):
                continue
            else:
                skip_parens = False

        if last is None:
            if ttype == '1':
                first_num = True
                last = t
                yield t
            else:
                #print "yeilding ", t
                yield t

        elif last[0] == '1' and ttype == 'o' and t[1] in ('|', '&', '!', '+', '-', '~', '/', '%', '*', 'MOD', 'DIV'):
            last = t
            first_num = False
        elif last[0] == 'o' and ttype == '1':
            #first_num = False
            last = t
        else:
            if first_num:
                #first_num = False
                last = None
                yield t
            else:
                if last[0] == 'o':
                    yield last
                first_num = True
                last = None

                yield t

    if last and last[0] == 'o':
        yield last
    #if not first_num and last:
    #   yield last


class SQLexer:
    def __init__(self):
        # this handles variable types @foo   and foo@bar is not a word
        self.ascii_words_re = re.compile(r'[A-Z0-9_.\$]+')
        self.var_words_re = re.compile(r'@@?[A-Z0-9_.\$]*')


        # [0-9]+\.?[0-9]*   int or plain float
        #    (E[+-]?[0-9])?  followed by optional exponent E+9 E2 E-10
        # special case starts with '.'
        #    \.[0-9]+    .1234
        #      again followed by optional E
        self.numeric_re = re.compile(r'((0X[0-9A-F]*)|([0-9]+\.?[0-9]*(E[+-]?[0-9])?)|(\.[0-9]+(E[+-]?[0-9])?))')

        self.map_main_alt = (
            self.parseWhite, # 0
            self.parseWhite, # 1
            self.parseWhite, # 2
            self.parseWhite, # 3
            self.parseWhite, # 4
            self.parseWhite, # 5
            self.parseWhite, # 6
            self.parseWhite, # 7
            self.parseWhite, # 8
            self.parseWhite, # 9
            self.parseWhite, # 10
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite, # 20
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite,
            self.parseWhite, #30
            self.parseWhite,               # 31
            self.parseWhite,               # 32
            self.parse_operator2,          # 33 !
            self.parseString,              # 34 "
            self.parseEOLComment,          # 35 "#"
            self.parseWord,                # 36 $
            self.parseSingleCharOperator,  # 37 %
            self.parse_operator2,          # 38 &
            self.parseString,              # 39 '
            self.parseChar,                # 40 (
            self.parseChar,                # 41
            self.parse_operator2,          # 42 *, '*' or '*/'
            self.parseSingleCharOperator,  # 43 +
            self.parseChar,                # 44 ,
            self.parseDashOperator,        # 45 -
            self.parse_numeric,            # 46 .
            self.parseSlashOperator,       # 47 /
            self.parse_numeric,            # 48 0
            self.parse_numeric,            # 49 1
            self.parse_numeric,            # 50 2
            self.parse_numeric,            # 51 3
            self.parse_numeric,            # 52 4
            self.parse_numeric,            # 53 5
            self.parse_numeric,            # 54 6
            self.parse_numeric,            # 55 7
            self.parse_numeric,            # 56 8
            self.parse_numeric,            # 57 9
            self.parseChar,                # 58 : colon
            self.parseChar,                # 59 ; semicolon
            self.parse_operator2,          # 60 <
            self.parse_operator2,          # 61 =
            self.parse_operator2,          # 62 >
            self.parseNone,                # 63 ?   BEEP BEEP
            self.parse_var,                # 64 @
            self.parseWord,                # 65 A
            self.parseWord,                # 66 B
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # Z
            self.parseChar,            # [
            self.parse_backslash,      # \\
            self.parseChar,            # ]
            self.parseSingleCharOperator, # ^
            self.parseWord,             # _
            self.parseWhite,             # backtick
            self.parseWord,            # A
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # @
            self.parseWord,            # z
            self.parseChar,            # brace
            self.parse_operator2,      # pipe
            self.parseChar,            # brace
            self.parseSingleCharOperator,
            self.parseWhite
            )

    def tokenize(self, newstr, delim):
        map_main_alt  = self.map_main_alt
        self.pos = 0
        self.s = newstr

        if delim != '':
            yield self.parseInitialString(delim)

        while self.pos < len(self.s):
            try:
                charval = ord(self.s[self.pos])
                parser = map_main_alt[charval]
                token = parser()
                if token:
                    yield token
            except IndexError:
                #print 'IndexError: got %s using %s' % ( self.s[self.pos], str(parser))
                self.pos += 1

    def parse_numeric(self):
        mo = self.numeric_re.search(self.s, self.pos)
        if mo:
            word = mo.group(1)
            self.pos += len(word)
            return ('1', word)
        elif self.s[self.pos] == '.':
            self.pos += 1
            return ('n', '.')
        else:
            print "FAIL: " + self.s[self.pos:]

    def parseWhite(self):
        """ just skips """
        self.pos += 1
        return None

    def parseChar(self):
        """ just skips """
        char =  self.s[self.pos]
        self.pos += 1
        return (char, char)

    def parseNone(self):
        """ just skips """
        char = self.s[self.pos]
        self.pos += 1
        return ('n', char)

    def parseSingleCharOperator(self):
        char = self.s[self.pos]
        self.pos += 1
        return ('o', char)

    def parseEOLComment(self):
        pos = self.pos
        endpos = self.s.find("\n", pos)
        if endpos == -1:
            word = self.s[pos:]
            self.pos = len(self.s)
        else:
            word = self.s[pos:endpos]
            self.pos = endpos + 1
        return ('c', word)

    def parseDashOperator(self):
        pos = self.pos
        if self.s[pos:pos+2] == '--':
            self.pos += 2
            return self.parseEOLComment()
        else:
            self.pos += 1
            return ('o', '-')

    def parse_backslash(self):
        # http://dev.mysql.com/doc/refman/5.0/en/null-values.html
        if self.pos+1 < len(self.s) and self.s[self.pos+1] == 'N':
            self.pos += 2
            return ('k', 'NULL')
            # note "select \Nx" == "select \N as x"
            # not sure it matters
        else:
            self.pos += 1
            return ('\\', '\\')

    # return 0 is not a comment
    # return 1 is plain "!" comment
    # return 6 !##### comment
    def isMySQLComment(self):
        offset = 0
        try:
            if self.s[self.pos+2] != '!':
                return 0
            offset = 1
            # do we have a mysql version number?
            # will pop exception if goes past end of line
            # or if not integer
            aint = self.s[self.pos+3:self.pos+8]
            mysqlv = int(aint)
            offset = 6
        except:
            pass

        return offset

    def parseSlashOperator(self):
        # TODO: handle mysql /*! operator
        #   rewrites string

        if self.pos+1 == len(self.s) or self.s[self.pos+1] != '*':
            return self.parseSingleCharOperator()

        cstart = self.pos
        inc = self.isMySQLComment()

        # find normal */ closer
        if self.pos+2+inc >= len(self.s):
            endpos = -1
            mysqlcstart = -1
        else:
            endpos = self.s.find('*/', self.pos+2+inc)
            # mysql comments are closed on next opening token
            # /*! foo /*! bar */ ==> foo bar
            mysqlcstart = self.s.find('/*!', self.pos+2+inc)

        if mysqlcstart != -1 and mysqlcstart < endpos:
                # just remove the /*! or /*!00000 and continue
                self.s = self.s[0:self.pos] + ' ' + self.s[self.pos+2+inc:]
                return None

        if inc == 0:
            # NORMAL COMMENT
            if endpos == -1:
                # unterminated comment
                word = self.s[self.pos:]
                self.pos = len(self.s)
            else:
                word = self.s[self.pos:endpos+2]
                self.pos = endpos + 2
            return ('c', word)

        else:
            # MySQL COMMENT
            if endpos == -1:
                # easy, doesn't terminate
                # just skip over the comment
                self.pos += 2 + inc
            else:
                self.pos += 2 + inc
                #print "XXX: " + self.s[self.pos:]
                #self.s = self.s[0:self.pos] + ' ' + self.s[self.pos+2+inc : endpos] + ' ' + self.s[endpos+2:]
            return None

    def parse_operator2(self):
        dco = self.s[self.pos:self.pos+2]

        if dco == '<=' and self.s[self.pos:self.pos+3] == '<=>':
            self.pos += 3
            return  ('o', '<=>')
        elif dco == '*/':
            #  Special Hack for MYSQL style comments
            # instead of turning:
            # /*! FOO */  into FOO by rewriting the string, we
            # turn it into FOO */ and ignore the ending comment
            self.pos += 2
            #print "XXX: got */ " + self.s[self.pos:]
            return None
        elif dco in double_char_operators:
            self.pos += 2
            return ('o', dco)
        else:
            self.pos += 1
            return ('o', dco[0])

    # TODO  @"FOO" @`FOO` styles
    def parse_var(self):
        wtype = 'v'
        mo = self.var_words_re.match(self.s, self.pos)
        word = mo.group()
        if word == '@' or word == '@@':
            wtype = 'n'
        self.pos += len(word)
        return (wtype, word)

    def parseWord(self):
        mo = self.ascii_words_re.match(self.s, self.pos)
        word = mo.group()
        self.pos += len(word)

        wtype = keywords.get(word, None)
        if wtype is not None:
            return (wtype, word)

        wtype = 'n'
        if word[0] == '0':
            tmp = word[1:]
            # special case for mysql < 5.1 where /*!0 was indicator
            # of versioned comment. so /*!0FOO*/ => 'FOO'
            # Modern versions of mysql use /*!0FOO*/ ==> 0FOO
            # If we get 0SELECT want to map it back to SELECT

            wtype = keywords.get(tmp, None)
            if wtype is not None:
                word = tmp
            else:
                wtype = 'n'

        return (wtype, word)

    def parseInitialString(self, delim):
        while True:
            qpos = self.s.find(delim, self.pos)
            if qpos == -1:
                self.pos = len(self.s)
                word = self.s
                break
            elif qpos == 0:
                word = delim
                self.pos = 1
                break
            elif self.s[qpos-1] == "\\":
                self.pos = qpos+1
            else:
                word = self.s[self.pos:qpos+1]
                self.pos = qpos + 1
                break

        return ('s', word)

    def parseString(self):
        delim = self.s[self.pos]
        while True:
            qpos = self.s.find(delim, self.pos+1)
            if qpos == -1:
                word = self.s[self.pos:]
                self.pos = len(self.s)
                break
            elif self.s[qpos-1] != "\\":
                word = self.s[self.pos:qpos+1]
                self.pos = qpos + 1
                break
            else:
                self.pos = qpos
        return ('s', word)


class Attacker:
    def __init__(self):
        self.lex = SQLexer()
        self.alpha_re = re.compile(r'^\s*[A-Za-z0-9_]*\s*$')

        #  foo10" or foo1'  must start with letter to preven
        #  7" # .... which is likely a measurement, not sqli
        self.alpha_str_re = re.compile(r'^[A-Z][A-Z0-9_]+[\'\"]$')

    def type_string(self, s, tname, delim):

        tokens = constant_folding2(sql_syntax(self.lex.tokenize(s, delim)))
        #if False:
        # itertools for some reason devastes performance
        # and is slower than just making a whole list
        #take6 = list(itertools.islice(tokens,6))
        #    take6 = list(tokens)
        #else:
        # manual loop unrolling
        take6 = []
        try:
            take6.append(next(tokens))
            take6.append(next(tokens))
            take6.append(next(tokens))
            take6.append(next(tokens))
            take6.append(next(tokens))
            take6.append(next(tokens))
        except StopIteration:
            pass

        #take6 = list(itertools.islice(tokens,6))
        #take6 = list(tokens)
        (sqli, fullpat, pat, reason) =  self.patmatch(take6)

        if not sqli:
            #print 'False: %s %s in %s on full %s' % (tname, reason, pat, fullpat)
            return None
        else:
            #print 'False: %s matched' % (tname)
            pass

        return tname, pat, fullpat, take6, s

    def test(self, s):

        m = self.type_string(s, 'type1', '')
        if m:
            return m
        m = self.type_string(s, 'type2', "'")
        if m:
            return m
        m = self.type_string(s, 'type3', '"')
        if m:
            return m

        return None

    def qsv_normalize(self, s):
        while True:
            snew = unquote(s)
            if s == snew:
                break
            s = snew.upper()

        # common html cut-n-paste problem
        # we do NOT want to make this a '"'
        # since they one could attack by inserting &QUOT; which
        # SQL will know, but we'll think it's a "
        s = s.replace('&QUOT;', '"')
        s = s.replace('&#39;', '\'')
        return s

    def test_qs(self, qs):
        for (key, value) in parse_qsl(qs):
            if self.alpha_re.match(value):
                continue
            attack = self.test(self.qsv_normalize(value.upper()))
            if attack:
                return attack
        return None

    def is_valid_sql(self, pat, tokens=None):
        tlen = len(tokens)

        if tlen <= 2:
            if pat == 'sc' and not self.alpha_str_re.match(tokens[0][1]):
                return "gibberish"

            return None

        elif tlen == 3:
            if pat in ('sk1','1k1'):
                if (tokens[1][1] not in ('ORDER BY', 'GROUP BY', 'OWN3D BY')):
                    return "pat is string-k-number but k not order/group by"

            elif pat == '1ok':
                # sqli fragment
                if tokens[1][1] not in ( 'UNION', 'UNION ALL'):
                    return 'too short'

            elif pat == 'sos':
                if tokens[1][1] in ('*', '/', '-', '+'):
                    return 'too small, harmless'

                isnormal_left = tokens[0][1][0] in ('"',"'")
                isnormal_right = tokens[2][1][-1] in ('"',"'")
                isempty_right = len(tokens[2][1]) == 1
                isenglish = tokens[1][1] in ('AND','&','NOT','UNION','IS','MOD')
                if isenglish:
                    # open string  ...foo "LIKE"
                    return "pat is string-operator-string and operator is logical"
                elif isnormal_left and isnormal_right:
                    # "FOO" + "BAR", type1 style
                    return "fully formed type1 sos -- ignoring"
                elif not isnormal_left and isempty_right:
                    return "not much of an attack"
                elif isnormal_left and not isnormal_right:
                    return "looks like truncation"
            return None
        elif tlen == 4:
            if pat == 'soos' and tokens[1][1] == tokens[2][1]:
                return "likely double typing or AND or OR"
            return None

        elif tlen == 5:
            if pat in ('so1on', 'no1oo'):
                return 'too short'
            elif pat in ('no1o1', '1ono1'):
                if tokens[1][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
                    return None
                else:
                    return 'bogon'
            elif pat[4] == 'f':
                return "ended in with function that requires parens"

            # NOT RETURN NONE... FALL THROUGH TO REMAINING CHECKS

        pat5 = pat[0:5]
        if pat5 in ('sonos', 'sono1', 'sosos', '1ono1', 'so1on', 'sonoo', 'no1o(', 'no1o1'):
            if tlen == 5 and tokens[1][1] != tokens[3][1] and tokens[1][1] not in ('&',):
                return None
            elif tokens[1][1] in ('UNION', 'UNION ALL'):
                return None
            elif tokens[1][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
                return None
            #elif tokens[3][1] in ('AND', 'OR', '&&', '||') and tokens[1][1] != tokens[3][1]:
            #    return None
            else:
                return "unlikely"

        elif tokens[4][0] == 'f' and tokens[5][0] != '(':
            return 'function not followed by parens'

        return None

    def patmatch(self, tokens):
        fullpat = ''.join([ t[0] for t in tokens ])
        pat = fullpat[0:5]
        if pat in sqlipat:
            oksql = self.is_valid_sql(fullpat, tokens)
            if oksql is None:
                return (True, fullpat, pat, '')
            else:
                return (False, fullpat, pat, oksql)
        return (False, fullpat, '', 'No starting pattern found')


import logging
from time import time

def dumbtest():
    at = Attacker()
    lex = SQLexer()
    imax = 1000000
    #imax = 1
    s = "123 LIKE -1234.5678E+2; APPLE 19.123 'FOO' /* bar */ UNION SELECT (2,3,4) || COS(+4) --FOOBAR"
    s = "F****'),(1,2,3,4,5,(SELECT IF ((ASCII(SUBSTRING(se_games.admin_pw,1,1)='1') & 1, benchmark(20000,CHAR(0)),0) FROM se_games))/*"
    s = "LIFE IS NOT ABOUT WAITING FOR THE STORM TO PASS"
    #s =  "BAR + - 1 1 * * BAR + 2 +"
    for i in xrange(imax):
        #x = list(constant_folding2(sql_syntax(lex.tokenize(s, ''))))
        at.test(s)
        #x = list(lex.tokenize(s, ''))
        #print x

def byline(fd, outfd):
    at = Attacker()

    tstart = time()
    t0= time()
    imax = 1000000
    count = 0

    for line in fd:
        #print line
        count += 1
        if count % imax  == 0:
            t1 = time()
            logging.debug("%d, Lap TPS: %d, Lap: %f, Elapsed TPS: %d, Elapsed: %f" % (count, int(imax/(t1-t0)), t1-t0, int(count/(t1 - tstart)), (t1-tstart)))
            t0= time()

        qs = line.strip()

        if False:
            # parse a raw query string
            attack = at.test_qs(qs)
        else:
            # for testing or raw values
            attack = at.test(at.qsv_normalize(unquote_plus(qs).upper()))

        if attack is not None:
            a1 = attack[4].replace("\n", "\\n")
            outfd.write("%s\t%s\t%s\n" % (attack[0],attack[1],a1,))
            outfd.flush()

    t1 = time()
    logging.debug("%d, Elapsed TPS: %d, Elapsed: %f" % (count, int(count/(t1 - tstart)), (t1-tstart)))

import sys

def bork(name, greenkey, reason):
    print "ABORTED: ", name, greenkey,reason
def optimize(name, loop, greenkey, operations):
    print "OPTIMIZE: ", name, loop, greenkey
def chook(jitdriver_name, loop_type, greenkey, operations, assembler_addr, assembler_length):
    if loop_type == 'entry bridge':
        print "COMPILE: ", loop_type, greenkey

if __name__ == '__main__':

    if False:
        import pypyjit
        pypyjit.set_abort_hook(bork)
        pypyjit.set_optimize_hook(optimize)
        pypyjit.set_compile_hook(chook)

    #dumbtest()
    #sys.exit(0)

    logging.basicConfig(level=logging.DEBUG)
    fd = sys.stdin
    outfd = sys.stdout
    byline(fd, outfd)
    #at = SQLexer()
    #for i in range(128):
    #    print i, chr(i), at.map_main_alt[i]
