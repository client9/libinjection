
# next

## security

* Fix for nested c-style comments used by postgresql and transact-sql.
  Thanks to @Kanatoko for the report.
* Numerous additions to SQL functions lists (in particular pgsql, transact-sql
  and ms-access functions)
  Thanks to Christoffer Sawicki "qerub" for report on cut-n-paste error.
  Thanks to @ryancbarnett for reminder that MS-ACCESS exists ;-)
* Adding of fingerprints to detect HPP attacks.  This may need
  fine tuning to reduce false positives later.
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

