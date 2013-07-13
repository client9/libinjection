# v3.3.0 2013-07-13
* change how backslash is handled to catch old MSSQL servers sqli
  See http://websec.ca/kb/sql_injection#MSSQL_Allowed_Intermediary_Chars_AND-OR
  for details

# v3.2.0 2013-07-12

* Parse binary litterals "0b010101" used by at least mysql and pgsql
* Add fingerprints '1&EUE', '1&EkU' to work around ambiguous parsing rules
  "-1.for" == '-1.f OR' vs. '-1. FOR'  CREDIT @LightOS
* Add parsing rules for COLLATION in MySQL, CREDIT @LightOS
* Reduce false positives by removing all fingerprints that contained "sn"
* Improvement in handling MySQL 'binary' quasi-operator/type
* Improvements in folding
* Removed dependency on SWIG for installing python module

# v3.1.0 2013-07-02

* Fix for parsing Oracle numeric literals
* Fix for oracle whitespace with null char.
* Add unusual SQL join types to keywords lists
* Minor fixes to python API examples

# v3.0.0 2013-06-23

Big Release and Big Engine change.  Highly recommened

* Numerous evasions and false positives fixed!
* Tokenizer is now really dumb, and publically exposed.  See `libinjection_sqli_tokenize`.
* Folding engine completely rewritten to be simpler and easier to extend, debug, port.
* MySQL `backticks` now handled correctly
* @"var" and @'var' parsed correctly (mysql)
* ":=" operator parsed correctly
* non-ascii SQL variables and barewords handled correctly
* less false positives and those that are false positives
  are more "indeterminate cases" and are only in a few
  fingerprints
* autogeneration of fingerprints with trivial SQL variations
* support for pgsql $ strings
* support for oracle's q and nq strings
* support for mysql's n strings
* parsing stats exposed
* new swig bindings for python and lua, with callbacks into original scripting
  language for accept/reject of fingerprints (i.e. manage fingerprints in
  script, not C code)
* Imporved parsing of various special cases in MySQL
* Ban MySQL conditional comments.  If we find them, it's marked as SQLi immediately.
* Probably a bunch of other stuff too

# v2.0.4 2013-05-21 IMPORTANT

All users are advised to upgrade due to risk of DOS

## security
* more fingerprints, more tests
* Issue 34: fix infinite loop

# v2.0.3 2013-05-21

## security
* Add variations on '1U(((', thanks @LightOS
* Add automatically all varations on other cases of
  'parens padding'

# v2.0.2 2013-05-21

## security
* Added fingerprint 'nU(kn' and variations, thanks to
  discussion with @ModSecurity .

# v2.0.1 2013-05-21

## security
* Added fingerprint knknk, thanks @d0znpp

# v2.0.0 2013-05-17

Version 2 is more a software engineering release than SQLi.
The API, the code, and filenames are improved for embedded
use.  Please see the README.md file for details on use.

## security

* Fix Issue30: detection of more small sqli forms with fingerprint "1c".
* Fix Issue32: false positive of '*/*' of type 'oc'  Thanks to @brianrectanus

## API Changes

BIG CHANGES

* File name changes.  These are the only relevant files:
   * `c/libinjection.h`
   * `c/libinjection_sqli.c`
   * `c/libinjection_sqli_data.h`
   * `COPYING`
* Just need to include `libinjection.h` and link with `libinjection_sqli_.c`
* `sqlparse_private.h` and `sqli_fingerprints.h` are deprecated.
   Only use `#include "libinjection.h"`
* API name changes `is_sqli` and `is_string_sqli` are now
  `libinjection_is_sqli` and `libinjection_is_string_sqli`
* API change, `libinjection_is_sqli` now takes a 5th arg for callback data
* API change, `libinjection_is_sqli` accepts `NULL` for arg4 and arg5
  in which case, a default lookup of fingerprints is used.
* `sqlmap_data.json` now includes fingerprint information, so people making
  ports only need to parse one file.

## other

* Allow `clang` compiler (also in Jenkins, a build with clang and
  make-scan is done)
* Optimizations should result in > 10% performance improvement
  for normal workloads
* Add `sqlite3` special functions and keywords (since why not)

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

