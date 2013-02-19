libinjection
============

SQL / SQLI tokenizer parser analyzer.

See
[http://www.client9.com/projects/libinjection/](http://www.client9.com/projects/libinjection/)
for details and presentations.

To use:
look at sqli_cli.cpp, reader.c as examples, but it's as simple as this:

    #include "sqlparse.h"

    // state data structure
    sfilter sf;

    // clean up input... always makes input smaller.
    len = sqli_qs_normalize(linebuf, len);

    // test it.  1 = is isql, 0 = benign
    bool issqli = is_sqli(&sf, linebuf, len);

    // sfilter now also has interesting details
    //   the fingerprint
    //   tokens
    //   etc
    // details to come

Copyright (c) 2012 Nick Galbreath
Licensed under standard BSD open source license
See /COPYING.txt -- commercial licenses available.
Send requests to nickg@client9.com

