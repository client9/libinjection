LIBINJECTION
==========================

Libinjection is a small C library to detect SQLi attacks in user input with the following goals:

* Open.  Source code is open, tests cases are open.
* Low _false-postives_.   When there are high false positives, people tend to turn it off.
* Excellent detection of SQLi.
* High performance, almost free.
* Easy to test and QA
* Easy to integrate and extend

Curious?  See more details below or:

* Try it now on the [diagnostics page](/diagnostics)
* Join the [Google Group](https://groups.google.com/d/forum/libinjection) to get updates
* Read the [FAQ](/faq-sqli)
* Download the [code](https://github.com/client9/libinjection/)

### Open Source

* Open source, code is on [GitHub](https://github.com/client9/libinjection/)
* [BSD License](https://github.com/client9/libinjection/blob/master/COPYING.txt)

### Easy to integrate

* Standard C code, and compiles as C99 and C++
* Compiles on Linux/Unix/BSD, Mac and Windows
* No threads used and thread safe
* No (heap) memory allocation
* Small - about 1200 lines of code in three files
* No extenal library dependencies

### Bindings to Scripting Langauges

* Python
* Lua

Third-Party Ports
---------------------

* [java](https://github.com/Kanatoko/libinjection-Java
* At least two .NET ports exists
* Another python wrapper

Applications
---------------------

* [ModSecurity](http://www.modsecurity.org/) - since 2.7.4 release
* [IronBee](https://www.ironbee.com) - since May 2013
* Proprietary Honeypot
* Proprietary WAF, Russia
* Proprietary WAF, Japan

Other
---------------------

* [a mention on Reddit](http://www.reddit.com/r/netsec/comments/x5pmr/libinjection_c_library_to_detect_sqli_attacks/) Reddit
