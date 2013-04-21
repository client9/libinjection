#!/usr/bin/env python
#
#  Copyright 2012, Nick Galbreath
#  nickg@client9.com
#  BSD License -- see COPYING.txt for details
#

"""
Converts a libinjection JSON data file to a C header (.h) file
"""

def toc(obj):
    """ main routine """

    print "#ifndef _SQLPARSE_DATA_H"
    print "#define _SQLPARSE_DATA_H"
    print "#include \"sqlparse.h\""
    print

    print 'static const char* operators2[] = {'
    for  k in sorted(list(obj[u'operators2'])):
        print '    "%s",' % (k,)
    print '};'
    dlen = len(obj['operators2'])
    print 'static const size_t operators2_sz = %d;' % (dlen,)
    print

    # keywords
    #
    keywords = obj['keywords']

    print "static const keyword_t sql_keywords[] = {"
    for k in sorted(keywords.keys()):
        print "    {\"%s\", '%s'}," % (k, keywords[k])
    print "};"
    print "static const size_t sql_keywords_sz = %d;" % (len(keywords), )


    #
    # compound keywords
    #
    phrases = obj['phrases']
    multikeywords_start = set()
    for words in phrases.iterkeys():
        parts = words.split(' ')
        plen = len(parts)
        multikeywords_start.add(parts[0])
        if plen == 3:
            multikeywords_start.add(parts[0] + ' ' + parts[1])

    print "static const char* multikeywords_start[] = {"
    for k in sorted(list(multikeywords_start)):
        print "    \"%s\"," % (k)
    print "};"

    dlen = len(multikeywords_start)
    print "static const size_t multikeywords_start_sz = %d;" % (dlen,)

    print "static const keyword_t multikeywords[] = {"
    for k in sorted(phrases.keys()):
        print "    {\"%s\", '%s'}," % (k, phrases[k])
    print "};"
    print "static const size_t multikeywords_sz = %d;" % (len(phrases), )

    #
    # Mapping of character to function
    #
    fnmap = {
        'CHAR_WORD': 'parse_word',
        'CHAR_WHITE': 'parse_white',
        'CHAR_OP1': 'parse_operator1',
        'CHAR_OP2': 'parse_operator2',
        'CHAR_BACK': 'parse_backslash',
        'CHAR_DASH': 'parse_dash',
        'CHAR_STR': 'parse_string',
        'CHAR_COM1': 'parse_eol_comment',
        'CHAR_NUM': 'parse_number',
        'CHAR_SLASH': 'parse_slash',
        'CHAR_CHAR': 'parse_char',
        'CHAR_VAR': 'parse_var',
        'CHAR_OTHER': 'parse_other',
        'CHAR_MONEY': 'parse_money'
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
    print "#endif"
    return 0

if __name__ == '__main__':
    import sys
    import json
    sys.exit(toc(json.load(sys.stdin)))

