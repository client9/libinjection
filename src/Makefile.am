include_HEADERS = libinjection.h

lib_LTLIBRARIES = libinjection.la
libinjection_la_SOURCES = libinjection_sqli.c libinjection_html5.c libinjection_xss.c
libinjection_la_CPPFLAGS = -I$(top_srcdir)/src

noinst_PROGRAMS = reader sqli testdriver testspeed testspeedxss

reader_SOURCES = reader.c
reader_CPPFLAGS = -I$(top_srcdir)/src
reader_LDADD = libinjection.la

sqli_SOURCES = sqli_cli.c
sqli_CPPFLAGS = -I$(top_srcdir)/src
sqli_LDADD = libinjection.la

testdriver_SOURCES = testdriver.c
testdriver_CPPFLAGS = -I$(top_srcdir)/src
testdriver_LDADD = libinjection.la

testspeed_SOURCES = test_speed.c
testspeed_CPPFLAGS = -I$(top_srcdir)/src
testspeed_LDADD = libinjection.la

testspeedxss_SOURCES = test_speed_xss.c
testspeedxss_CPPFLAGS = -I$(top_srcdir)/src
testspeedxss_LDADD = libinjection.la
