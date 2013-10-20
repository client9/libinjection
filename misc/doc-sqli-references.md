SQLi References
===========================

SQLi References and Cheatsheets
-------------------------------

* [Websec.ca SQLI KB Cheatsheet](http://websec.ca/kb/sql_injection)  Highly recommended.
* [OWASP SQLi Introduction](https://www.owasp.org/index.php/SQL_Injection)


SQLi Detection
--------------

_Stephen W. Boyd and Angelos D. Keromytis, [SQLrand: Preventing SQL Injection Attacks](http://www1.cs.columbia.edu/~angelos/Papers/sqlrand.pdf), Proceedings of the 2nd Applied Cryptography and Network Security (ACNS) Conference, 2004_

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

This requires rewriting all queries in the application,
installing a new proxy between your clients and database.

---

_Robert J. Hansen, Meredith L. Patterson, [Guns and Butter: Towards Formal Axioms of Input Validation](http://www.blackhat.com/presentations/bh-usa-05/BH_US_05-Hansen-Patterson/HP2005.pdf), presentation at Black Hat 2005, 2005-06-30_

Key points:

* Using regular expressions to parse a high-order language will always produce false-positives and false-negatives
* Uses a tree based a approach to detect when user input changes the SQLi structure.
* POC implementaton done using psql parser http://sourceforge.net/projects/libdejector/

---
_Gregory T. Buehrer , Bruce W. Weide , Paolo A. G. Sivilotti, [Using parse tree validation to prevent SQL injection attacks](http://www.cse.ohio-state.edu/~paolo/research/publications/sem05.pdf), Proceedings of the International Workshop on Software Engineering and Middleware (SEM) at Joint FSE and ESEC, 2005_

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

_W. Halfond and A. Orso, [AMNESIA: Analysis and Monitoring for NEutralizing SQL-Injection Attacks](http://www-bcf.usc.edu/~halfond/papers/halfond05ase.pdf), Automated Software Engineering, 2005_

Homepage: http://www-bcf.usc.edu/~halfond/amnesia.html

This appears to use static analysis to indentify SQL query creation
points ("hotspots") in Java code.  It then instruments the code to do
tree analysis before and after user input.

This appears to require no change in the development process (that's good),
and only adding a compile step (?).  Worth investigating more.

---

_Christian Bockerman [Protecting Databases with Trees](http://es.slideshare.net/hashdays/hashdays-2011-christian-bockermann-protecting-databases-with-trees), presentation at HashDays 2011_

Another Tree-based with additional statistics and training.  Note last slide "Writing SQL parsers is hard"

