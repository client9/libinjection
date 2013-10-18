LIBINJECTION
==========================

Libinjection is a small C library to detect SQLi attacks in user input with the following goals:

* Open.  Source code is open, tests cases are open.
* Low _false-postives_.   When there are high false positives, people tend to turn off any WAF or protection.
* Excellent detection of SQLi.
* High performance, almost free.
* Easy to test and QA
* Easy to integrate and extend

Curious?  See more details below or:

* Try it now on the [diagnostics page](/diagnostics)
* Read the [FAQ](/faq-sqli)
* Download the [code](https://github.com/client9/libinjection/)

### Open Source

* Open source, code is on [GitHub](https://github.com/client9/libinjection/)
* [BSD License](https://github.com/client9/libinjection/blob/master/COPYING.txt)

### Easy to integrate

* Standard C code, and compiles as C99 and C++
* Small - about [1500 lines of code](/cicada/artifacts/libinjection-loc/console.txt) in three files
* Compiles on Linux/Unix/BSD, Mac and Windows
* No threads used and thread safe
* No recursion
* No (heap) memory allocation
* No extenal library dependencies
* 400+ unit tests
* 98% code coverage

### Bindings to Scripting Langauges

* [Python](/doc-sqli-python)
* [PHP](/doc-sqli-php)
* [Lua](https://github.com/client9/libinjection/tree/master/lua)

Third-Party Ports
---------------------

* [java](https://github.com/Kanatoko/libinjection-Java)
* At least two .NET ports exists
* Another python wrapper

Applications
---------------------

* [ModSecurity](http://www.modsecurity.org/) - since 2.7.4 release
* [IronBee](https://www.ironbee.com) - since May 2013
* Proprietary Honeypot
* Proprietary WAF, Russia
* Proprietary WAF, Japan

