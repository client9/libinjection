#!/usr/bin/env python
#
#  Copyright 2012, 2013 Nick Galbreath
#  nickg@client9.com
#  BSD License -- see COPYING.txt for details
#

"""
Converts a libinjection JSON data file to a C header (.h) file
"""

def toc(obj):
    """ main routine """

    print """
#ifndef _LIBINJECTION_SQLI_DATA_H
#define _LIBINJECTION_SQLI_DATA_H

#include "libinjection.h"

typedef struct {
    const char *word;
    char type;
} keyword_t;

static size_t parse_money(sfilter * sf);
static size_t parse_other(sfilter * sf);
static size_t parse_white(sfilter * sf);
static size_t parse_operator1(sfilter *sf);
static size_t parse_char(sfilter *sf);
static size_t parse_hash(sfilter *sf);
static size_t parse_dash(sfilter *sf);
static size_t parse_slash(sfilter *sf);
static size_t parse_backslash(sfilter * sf);
static size_t parse_operator2(sfilter *sf);
static size_t parse_string(sfilter *sf);
static size_t parse_word(sfilter * sf);
static size_t parse_var(sfilter * sf);
static size_t parse_number(sfilter * sf);
static size_t parse_tick(sfilter * sf);
static size_t parse_underscore(sfilter * sf);
static size_t parse_ustring(sfilter * sf);
static size_t parse_qstring(sfilter * sf);
static size_t parse_nqstring(sfilter * sf);
static size_t parse_xstring(sfilter * sf);
static size_t parse_bstring(sfilter * sf);
static size_t parse_estring(sfilter * sf);
"""

    #
    # Mapping of character to function
    #
    fnmap = {
        'CHAR_WORD' : 'parse_word',
        'CHAR_WHITE': 'parse_white',
        'CHAR_OP1'  : 'parse_operator1',
        'CHAR_OP2'  : 'parse_operator2',
        'CHAR_BACK' : 'parse_backslash',
        'CHAR_DASH' : 'parse_dash',
        'CHAR_STR'  : 'parse_string',
        'CHAR_HASH' : 'parse_hash',
        'CHAR_NUM'  : 'parse_number',
        'CHAR_SLASH': 'parse_slash',
        'CHAR_CHAR' : 'parse_char',
        'CHAR_VAR'  : 'parse_var',
        'CHAR_OTHER': 'parse_other',
        'CHAR_MONEY': 'parse_money',
        'CHAR_TICK' : 'parse_tick',
        'CHAR_UNDERSCORE': 'parse_underscore',
        'CHAR_USTRING'   : 'parse_ustring',
        'CHAR_QSTRING'   : 'parse_qstring',
        'CHAR_NQSTRING'  : 'parse_nqstring',
        'CHAR_XSTRING'   : 'parse_xstring',
        'CHAR_BSTRING'   : 'parse_bstring',
        'CHAR_ESTRING'   : 'parse_estring'
        }
    print
    print "typedef size_t (*pt2Function)(sfilter *sf);"
    print "static const pt2Function char_parse_map[] = {"
    pos = 0
    for character in obj['charmap']:
        print "   &%s, /* %d */" % (fnmap[character], pos)
        pos += 1
    print "};"
    print

    # keywords
    #  load them
    keywords = obj['keywords']

    for  fp in list(obj[u'fingerprints']):
        fp = '0' + fp.upper()
        keywords[fp] = 'F';

    mysqlunicodecollations = (
        '_bin',
        '_czech_ci',
        '_danish_ci',
        '_esperanto_ci',
        '_estonian_ci',
        '_general_ci',
        '_general_mysql500_ci',
        '_hungarian_ci',
        '_icelandic_ci',
        '_latvian_ci',
        '_lithuanian_ci',
        '_persian_ci',
        '_polish_ci',
        '_roman_ci',
        '_romanian_ci',
        '_sinhala_ci',
        '_slovak_ci',
        '_slovenian_ci',
        '_spanish_ci',
        '_spanish2_ci',
        '_swedish_ci',
        '_turkish_ci',
        '_unicode_ci')

    unicodes = ('ucs2', 'utf16', 'utf32', 'utf8', 'utf8mb4')

    for k in mysqlunicodecollations:
        for j in unicodes:
            keywords[j + k] = 't'

    needhelp = []
    for k,v in keywords.iteritems():
        if k != k.upper():
            needhelp.append(k)

    for k in needhelp:
        v = keywords[k]
        del keywords[k]
        keywords[k.upper()] = v

    print "static const keyword_t sql_keywords[] = {"
    for k in sorted(keywords.keys()):
        print "    {\"%s\", '%s'}," % (k, keywords[k])
    print "};"
    print "static const size_t sql_keywords_sz = %d;" % (len(keywords), )

    print "#endif"
    return 0

if __name__ == '__main__':
    import sys
    import json
    sys.exit(toc(json.load(sys.stdin)))

