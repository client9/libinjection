libinjection SQLi False Positives
=================================

Some very benign looking queries are sometimes flagged as SQLi.  This
can be due to the nature of SQL, and how some databases process it.
As an example:

    I 'LIKE' YOU

could be considered SQLi and can be used to scan the contents of a
table (In this case it is the `LIKE` operator with two strings).

Fortunately, most false-positives like this are limited to a few
fingerprints and can be turned off without affecting detection of
other SQLi attacks.

How to do I turn off a particular fingerprint
---------------------------------------------

TK

What are common False Positives
--------------------------------

TK: Current False positives on Jenkins

How do I report a false positive?
---------------------------------

The best way is by filling a bug report on [GitHub](https://github.com/client9/libinjection/issues), or a new message on [Google Groups](https://groups.google.com/d/forum/libinjection).

Please include:

* The WebServer and Platform you are using (some platforms alter characters)
* The full query string
* Any information you have on the character encoding (is this UTF-8? or something else?)
* Your Twitter name or other contact details if your want [public credit](/bypass).
