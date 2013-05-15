libinjection
============

SQL / SQLI tokenizer parser analyzer.

See
[http://www.client9.com/projects/libinjection/](http://www.client9.com/projects/libinjection/)
for details and presentations.

To use:
look at sqli_cli.cpp, reader.c as examples, but it's as simple as this:

```c
#include "libinjection.h"

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
    // The last arg control how fingerprints are matched
    // with SQLi.  The last args of "NULL, NULL"  means
    //  use the default built-in list.
    bool issqli = libinjection_is_sqli(&sf, linebuf, len, NULL, NULL);

    // sfilter now also has interesting details
    //   the fingerprint
    //   tokens
    //   etc
}
```

VERSION INFORMATION
===================

Current version is 1.2.0 released on 2013-05-06.

See [CHANGELOG](/CHANGELOG.md) for details.

Versions are listed as "major.minor.point"

Major are significant changes to the API and/or fingerprint format.
Applications will need recompiling and/or refactoring.

Minor are C code changes.  These may include
 * logical change to detect or suppress
 * optimization changes
 * code refactoring

Point releases are purely data changes.  These may be safely applied.

QUALITY AND DIAGNOSITICS
========================

Use the diagnostic test page at

https://libinjection.client9.com/diagnostics

For quick experiments, cracking and breaking, and other ad-hoc tests.

At https://libinjection.client9.com/jenkins/view/libinjection/ is
a [Jenkin](http://jenkins-ci.org/) server showing automated testing:

* build and unit-tests under GCC latest
* build, unit-tests and static analysis using clang
* results from cppcheck (static analysis on C code)
* results from pylint and pyflake (static analysis on python helper scripts)
* results from valgrind (memory errors)
* performance tests using grof
* false negatives and positives reports

LICENSE
=============

Copyright (c) 2012,2013 Nick Galbreath

Licensed under the standard BSD open source license.  See [COPYING.txt](/COPYING.txt) for details.

Commercial and support licenses available.

Send requests to nickg@client9.com


EMBEDDING
=============

The 'c' directory is a mess, but you only need to copy the following
into your source tree:

* c/libinjection.h
* c/libinjection_sqli.c
* c/libinjection_sqli_data.h
* COPYING

