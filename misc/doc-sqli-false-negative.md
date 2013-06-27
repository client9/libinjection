libinjection SQLi False Negatives
=================================

Here are some common reasons why a 'false negative' might be occurring:

### Input isn't valid SQL

If the input is unlikely to be a valid SQL fragment, then
libinjection will not mark it as SQLi.  In other words, if it won't
successfully execute an attack, it's not marked as SQLi.  It will likely
cause a syntax error or some other error in the database and those
can be detected in a different way.

Many SQLi scanners emit invalid SQL or broken SQL, and it's very easy
to make invalid SQL if you are manually hacking.

This may be unlike other WAFs you have that used that do "if it looks
like SQLi, then it is SQLi".  libinjection actually checks to make
sure it _is_ sql.

There are a few invalid SQLi inputs that are detected anyway, mostly
as a preventative measure in case of coding mistakes or incomplete SQL
parsing.


### URL-decoding problems and use of '+'

If modifying the query string directly, please check to make sure that
'+' are being correctly being decoded into '+' and not a space
character.  When this happens, the SQL is frequently modified into
something that will cause a syntax error and will not be detected.
Try changing the use of '+' to '-' and see if this helps.

### Use of fancy unicode quotes

A SQLi example that is cut-n-paste from a Wordpress site frequently
has fancy unicode quotes instead of normal single or double
quotes. For example, [this report][cve20132397] has the SQLi [1][bad1],
[2][bad2] that start with:

    1′) UNION ALL SELET

Note the Unicode character -- that's not a ASCII " or a '. These
alternative quotes are not recognized by any SQL engine.  Converting
the Unicode quotes to single or double quote normally allows detection
to proceed normally.  For example, the corrected queries [1][fix1],
[2][fix2] are detected correctly.

[cve20132397]: http://penturalabs.wordpress.com/2013/06/18/oracle-sqli-advisory-cve-2013-2397/

[bad1]: /diagnostics?id=1′%29+UNION+ALL+SELECT+%0D%0ACHR%2858%29+%7C%7C+CHR%28112%29+%7C%7C+CHR%28111%29+%7C%7C+CHR%28109%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2875%29+%7C%7C+CHR%2876%29+%7C%7C+CHR%2890%29+%7C%7C+CHR%2877%29+%7C%7C+CHR%2868%29+%7C%7C+CHR%2883%29+%7C%7C+CHR%2899%29+%7C%7C+CHR%2888%29+%7C%7C+CHR%28104%29+%7C%7C+CHR%28103%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2897%29+%7C%7C+CHR%28108%29+%7C%7C+CHR%28117%29+%7C%7C+CHR%2858%29%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL+FROM+DUAL+--

[bad2]: /diagnostics?id=1′%29+UNION+ALL+SELECT+%0D%0ACHR%2858%29+%7C%7C+CHR%28112%29+%7C%7C+CHR%28111%29+%7C%7C+CHR%28109%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2875%29+%7C%7C+CHR%2876%29+%7C%7C+CHR%2890%29+%7C%7C+CHR%2877%29+%7C%7C+CHR%2868%29+%7C%7C+CHR%2883%29+%7C%7C+CHR%2899%29+%7C%7C+CHR%2888%29+%7C%7C+CHR%28104%29+%7C%7C+CHR%28103%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2897%29+%7C%7C+CHR%28108%29+%7C%7C+CHR%28117%29+%7C%7C+CHR%2858%29%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL+FROM+DUAL+--

[fix1]: /diagnostics?id=1%27%29+UNION+ALL+SELECT+%0D%0ACHR%2858%29+%7C%7C+CHR%28112%29+%7C%7C+CHR%28111%29+%7C%7C+CHR%28109%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2875%29+%7C%7C+CHR%2876%29+%7C%7C+CHR%2890%29+%7C%7C+CHR%2877%29+%7C%7C+CHR%2868%29+%7C%7C+CHR%2883%29+%7C%7C+CHR%2899%29+%7C%7C+CHR%2888%29+%7C%7C+CHR%28104%29+%7C%7C+CHR%28103%29+%7C%7C+CHR%2858%29+%7C%7C+CHR%2897%29+%7C%7C+CHR%28108%29+%7C%7C+CHR%28117%29+%7C%7C+CHR%2858%29%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL%2C+NULL+FROM+DUAL+--

[fix2]: /diagnostics?id=1%27%29+AND+1684%3DDBMS_PIPE.RECEIVE_MESSAGE%28CHR%2875%29+%7C%7C+CHR%28106%29+%7C%7C+CHR%2890%29+%7C%7C+CHR%28100%29%2C5%29+AND+%28%27TGzC%27%3D%27TGzC%27

### The SQLi is really short

A few very short SQLi might not be detected due to a high
incidence of false positives, or inability to tell if the input is
malicious or just normal input.  Most of these SQLi examples are
fairly benign and not interesting.

### You found a true bypass!

Congratulations.  Please tell us more using the [next section](#how_do_i_report_a_bypass).

How do I report a bypass?
-------------------------

The best way is filing a bug report on [GitHub](https://github.com/client9/libinjection/issues), or a new
message on [Google Groups](https://groups.google.com/d/forum/libinjection).

Please include:

* The database and database version you think you are using.
* The full SQL query with your injection.
* Any information character encoding (is this UTF-8? or something else)
* Your twitter or other contact details if your want [public credit](/bypass).

Ideally you can cut-n-paste the output from the database.

Thanks!
