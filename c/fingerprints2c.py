#!/usr/bin/env python
#
#  Copyright 2012, Nick Galbreath
#  nickg@client9.com
#  BSD License -- see COPYING.txt for details
#
"""
Turns a fingerprints.txt into a C header (.h) file
"""

def main():
    """
    main routine, prints to stdout
    """

    print "#ifndef _SQLPARSE_FINGERPRINTS_H"
    print "#define _SQLPARSE_FINGERPRINTS_H"
    print

    with open('fingerprints.txt', 'r') as fd:
        sqlipat = [ line.strip() for line in fd ]

    print 'static const char* patmap[] = {'
    for k in sorted(sqlipat):
        print '    "%s",' % (k,)
    print '};'
    print 'static const size_t patmap_sz = %d;' % (len(sqlipat))
    print

    print """
/* Simple binary search */
int is_sqli_pattern(const char *key)
{
    int left = 0;
    int right = (int)patmap_sz - 1;

    while (left <= right) {
        int pos = (left + right) / 2;
        int cmp = strcmp(patmap[pos], key);
        if (cmp == 0) {
            return 1; /* TRUE */
        } else if (cmp < 0) {
            left = pos + 1;
        } else {
            right = pos - 1;
        }
    }
    return 0; /* FALSE */
}
"""

    print "#endif"

if __name__ == '__main__':
    main()
