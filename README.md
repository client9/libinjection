libinjection
============

SQL / SQLI tokenizer parser analyzer.

See
[http://www.client9.com/projects/libinjection/](http://www.client9.com/projects/libinjection/)
for details and presentations.

To use:
look at sqli_cli.cpp, reader.c as examples, but it's as simple as this:



```c
#include "sqlparse.h"
#include "sqli_fingerprints.h"

void doit() {

    // state data structure
    sfilter sf;

    // if you need to, normalize input.
    // in the case of a raw query string, url-decode the input
    // you can use this function (included in "modp_burl.h")
    len = modp_urldecode(linebuf, len);

    // test it.  1 = is sqli, 0 = benign
    // input is const (not changed or written to)
    //
    // 'is_sqli_pattern' is just a function that does a binary
    // search on a hardwired set of fingerprints.  One can
    // over-ride this function to read the fingerprints from a
    // file, or a hash table or from a scripting langauge.
    bool issqli = is_sqli(&sf, linebuf, len, is_sqli_pattern);

    // sfilter now also has interesting details
    //   the fingerprint
    //   tokens
    //   etc
}
```

VERSION INFORMATION
===================

Current version is 1.1.0.  See [CHANGELOG](/CHANGELOG.md) for details.

Versions are listed as "major.minor.point"

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

Licensed under the standard BSD open source license.  See [COPYING.txt](/COPYING.txt) for details.

Commercial and support licenses available.

Send requests to nickg@client9.com

