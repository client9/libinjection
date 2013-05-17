# vNext

# v2.0.0 2013-05-15

Version 2 is more a software engineering release than SQLi.
The API, the code, and filenames are improved for embedded
use.  Please see the README.md file for details on use.

## security

* Fix Issue30: detection of more small sqli forms with fingerprint "1c".
* Fix Issue32: false positive of '*/*' of type 'oc'  Thanks to @brianrectanus

## API Changes

BIG CHANGES

* File name changes.  These are the only relevant files:

   * libinjection.h
   * libinjection_sqli.c
   * libinjection_sqli_data.h

* Just need to include 'libinjection.h' and link with 'libinjection_sqli_.c'
* sqlparse_private.h and sqli_fingerprints.h are deprecated.  One only needs
  to include 'libinjection.h'
* API name changes is_sqli and is_string_sqli are now 'libinjection_is_sqli' and
  'libinjection_is_sqli' and 'libinjection_is_string_sqli'
* API change, libinjection_is_sqli now takes a 5th arg for callback data
* API change, libinjection_is_sqli accepts NULL for arg4 and arg5
  in which case, a default lookup of fingerprints is used.
* sqlmap_data.json now includes fingerprint information, so people making ports
  only need to parse one file.

## other

* Allow clang compiler (also in Jenkins, a build with clang and
  make-scan is done)
* Optimizations should result in > 10% performance for normal workloads
* Add Sqlite3 special functions and keywords (since why not)

# v1.2.0 2013-05-06

## security
* fix regression in detecting SQLi of type '1c'

##
* improved documentation, comments, edits.

# v1.1.0 2013-05-04

## security

* Fix for nested c-style comments used by postgresql and transact-sql.
  Thanks to @Kanatoko for the report.
* Numerous additions to SQL functions lists (in particular pgsql, transact-sql
  and ms-access functions)
  Thanks to Christoffer Sawicki (GitHub "qerub") for report on cut-n-paste error.
  Thanks to @ryancbarnett for reminder that MS-ACCESS exists ;-)
* Adding of fingerprints to detect HPP attacks.
* Algorihmically added new fingerprints to detect new _future_ sqli attacks.  All of these
  new fingerprints have no been seen 'in the wild' yet.

## other

* Replaced BSD memmem with optimzed version.  This eliminates all 3rd party code.
* Added alpha python module (python setup.py install)
* Added sqlparse_fingerprints.h and sqlparse_data.json to aid porting and embeddeding.
* Added version number in sqlparse.h, based on
  http://www.python.org/dev/peps/pep-0386/#normalizedversion

# v1.0.0 2013-04-24

* retroactive initial release
* all memory issues fixed

