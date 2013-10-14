libinjection
============

SQL / SQLI tokenizer parser analyzer. For

* C and C++
* PHP
* Python
* Lua

See
[https://libinjection.client9.com/](https://libinjection.client9.com/)
for details and presentations.

To use:
look at sqli_cli.c, reader.c as examples, but it's as simple as this:

```c
#include <stdio.h>
#include <strings.h>
#include "libinjection.h"

int main(int argc, const char* argv[])
{
    sfilter state;
    int issqli

    const char* input = argv[1];
    size_t slen = strlen(input);

    /* in real-world, you would url-decode the input, etc */

    libinjection_sqli_init(&state, input, slen, FLAG_NONE);
    issqli = libinjection_is_sqli(&state);
    if (issqli) {
        fprintf(sterr, "sqli detected with fingerprint of '%s'\n", state.pat);
    }
    return issqli;
}
```

```
$ gcc examples.c libinjection_sqli.c
$ ./a.out "-1' and 1=1 union/* foo */select load_file('/etc/passwd')--"
sqli detected with fingerprint of 's&1UE'
```

VERSION INFORMATION
===================

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

At https://libinjection.client9.com/cicada/ is
a integration server showing automated testing:

* build and unit-tests under GCC latest
* build, unit-tests and static analysis using clang
* results from cppcheck (static analysis on C code)
* results from pylint and pyflake (static analysis on python helper scripts)
* results from valgrind (memory errors)
* performance tests using gprof
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

