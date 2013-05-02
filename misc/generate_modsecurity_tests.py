#!/usr/bin/env python

# This generates a perl file that can be used by ModSecurity's unit
# test infrastructure.
#
import glob

def doit():
    for fname in glob.glob('./sqli-*.txt'):
        with open(fname, 'rb') as fd:
            for line in fd:
                line = line.strip()
                if len(line) and line[0] != '#':
                    line = line.replace('\\', '\\\\"')
                    #line = line.replace("'", "\\'")
                    line = line.replace('"', '\\"')

                    line = line.replace('@', '\\@')
                    line = line.replace('$', '\\$')
                    print '{'
                    print '   type => "op",'
                    print '   name => "detectSQLi",'
                    print '   input => "' + line + '",'
                    print '   ret => 1'
                    print '},'

if __name__ == '__main__':
    doit()

