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

    // if you need to, normalize input.
    // in the case of a raw query string, you would url-decode the
    len = modp_urldecode(linebuf, len);

    // test it.  1 = is isql, 0 = benign
    // input is const (not changed or written to)
    bool issqli = is_sqli(&sf, linebuf, len);

    // sfilter now also has interesting details
    //   the fingerprint
    //   tokens
    //   etc


VERSION INFORMATION
===================

Version are listed as "major.minor.point"

Major are significant changes to the API and/or fingerprint format.
Applications will need recompiling and/or refactoring.

Minor are C code changes.  These may include
 * logical change to detect or suppress
 * optimization changes
 * code refactoring

Point releases are purely data changes.  These may be safely applied.

LICENSE
=============

Copyright (c) 2012,2013 Nick Galbreath

Licensed under the standard BSD open source license.

See /COPYING.txt -- commercial and support licenses available.

Send requests to nickg@client9.com

