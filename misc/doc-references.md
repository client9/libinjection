References
===========================

libinjection
---------------------------

Black Hat USA 2012-07-24
http://www.client9.com/2012/07/25/libinjection/

DEFCON 20
[New Techniques in SQL Obfuscation](http://www.client9.com/2012/07/27/new-techniques-in-sql-obfuscation/)

iSec Partners Open Forum
[libinjection: New Techniques in Detecting SQLi Attacks](http://www.client9.com/2012/09/06/libinjection-new-techniques-in-detecting-sqli-attacks/)

OWASP NYC 2012-09-27:
libinjection and SQLi Obfuscation

RSA USA: 2013-02-27:
[SQL-RISC New Directions in SQLi Prevention](http://www.client9.com/2013/02/27/sql-risc-new-directions-in-sqli-prevention/)


libinjection mentions
---------------------------

[SQL Injection Obfuscation Libinjection](http://www.nsai.it/2012/11/21/sql-injection-obfuscation-libinjection/) in [National Security Alert Italia](http://www.nsai.it/), 2012-11-21


SQLi
---------------------------

### SQLi References and Cheatsheets

[OWASP SQLi Introduction](https://www.owasp.org/index.php/SQL_Injection)

### SQLi Detection

Stephen W. Boyd and Angelos D. Keromytis, [SQLrand: Preventing SQL Injection Attacks](http://www1.cs.columbia.edu/~angelos/Papers/sqlrand.pdf), Proceedings of the 2nd Applied Cryptography and Network Security (ACNS) Conference, 2004

Summary: The client rewrites all SQL queries by appending a fixed
number, e.g. `SELECT` becomes `SELECT123`.  A proxy in front of the
databases parses the incoming query using this new set of keywords.
If there is a syntax error then someone is inserting SQL.  For
example:

```
SELECT * FROM atable WHERE id=$id
```

becomes

```
SELECT123 * FROM123 atable WHERE123 id=$id
```

A simple attack might look like:

```
SELECT123 * FROM123 atable WHERE123 id= 1 UNION SELECT 1
```

The injection `1 UNION SELECT 1` now isn't using the new keywords, so
when the proxy parses it becomes a syntax error.  In otherwords, the
new query is effectively like this:

```
SELECT * FROM atable WHERE id= 1 blah foo 1
```

which won't execute.  The proxy then blocks this request.  Otherwise
it passes it back to the database.

No sample code released.

This requires rewritting all queries in the application,
installing a new proxy between your clients and database.

---

Robert J. Hansen, Meredith L. Patterson, [Guns and Butter: Towards Formal Axioms of Input Validation](http://www.blackhat.com/presentations/bh-usa-05/BH_US_05-Hansen-Patterson/HP2005.pdf), presentation at Black Hat 2005, 2005-06-30

Key points:

* Using regular expressions to parse a high-order language will always produce false-positives and false-negatives
* Uses a tree based a approach to detect when user input changes the SQLi structure.
* POC implementaton done using psql parser http://sourceforge.net/projects/libdejector/

---
Gregory T. Buehrer , Bruce W. Weide , Paolo A. G. Sivilotti, [Using parse tree validation to prevent SQL injection attacks](http://www.cse.ohio-state.edu/~paolo/research/publications/sem05.pdf), Proceedings of the International Workshop on Software Engineering and Middleware (SEM) at Joint FSE and ESEC, 2005.

Slides: http://www.cse.ohio-state.edu/~paolo/research/publications/sem05_talk.pdf

Software in Java: http://www.cse.ohio-state.edu/~paolo/software/,  uses http://zql.sourceforge.net/

You create SQL statements using

```
String q= "SELECT * FROM reports WHERE id = " + id;
```

One would do:

```
String q = SQLGuard.init() + "SELECT * FROM reports WHERE id = " + SQLGuard.wrap(id);
```

On execution it will create a parse tree of the original query
template and compare it to the new query.  If it doesn't match, it is
SQLi.

This requires rewriting all queries and using a new JDBC driver.  In
addition, I'm not sure how it actually prevents this development error:

```
String q = SQLGuard.init() + "SELECT * FROM reports WHERE id = " + id;
```

---

W. Halfond and A. Orso, [AMNESIA: Analysis and Monitoring for NEutralizing SQL-Injection Attacks](http://www-bcf.usc.edu/~halfond/papers/halfond05ase.pdf), Automated Software Engineering, 2005

Homepage: http://www-bcf.usc.edu/~halfond/amnesia.html

This appears to use static analysis to indentify SQL query creation
points ("hotspots") in Java code.  It then instruments the code to do
tree analysis before and after user input.

This appears to require no change in the development process (that's good),
and only adding a compile step (?).  Worth investigating more.

---

Christian Bockerman [Protecting Databases with Trees](http://es.slideshare.net/hashdays/hashdays-2011-christian-bockermann-protecting-databases-with-trees), presentation at HashDays 2011.

Another Tree-based with additional statistics and training.  Note last slide "Writing SQL parsers is hard"

---

XSS
---------------------------

[OWASP XSS Filter Evasion Cheat Sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet)

[IE's regular expressions XSS filters](http://xss.cx/examples/ie/internet-exploror-ie9-xss-filter-rules-example-regexp-mshtmldll.txt)

[Stackover on parsing XHTML with Regular Expressions](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454)
Comedy Gold

[StackExchange Discussion on Django's output filters](http://security.stackexchange.com/questions/34088/is-there-a-way-to-bypass-djangos-xss-escaping-with-unicode)
