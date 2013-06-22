libinjection SQLi False Positives
=================================

Due to the nature of SQL and how databases, some very benign looking
queries are sometimes flagged as SQLi.  As an example:

    I 'LIKE' YOU

While it looks benign, actually it will execute as a SQLi and can be
used to scan the contents of a table (the `LIKE` operator with two
strings).

Fortunately, most false-positives like this are limited to a few
fingerprints and can be turned off with out effecting detection of
other SQLi attacks.

How to do I turn off a particular fingerprint
---------------------------------------------

TK

What are common False Positives
--------------------------------

TK: Current False positives on Jenkins

How do I report a false positive?
---------------------------------

The best way is filing a bug report on[GitHub](https://github.com/client9/libinjection/issues), or a new message on [Google Groups](https://groups.google.com/d/forum/libinjection).

Please include:

* The WebServer and Platform you are using (some platforms alter characters)
* The full query string
* Any information you have on character encoding (is this UTF-8? or something else)
* Your twitter or other contact details if your want [public credit](/bypass).
