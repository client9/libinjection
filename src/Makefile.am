
include_HEADERS = libinjection.h

lib_LTLIBRARIES = libinjection.la
libinjection_la_SOURCES = libinjection.h \
	libinjection_sqli.h libinjection_sqli.c libinjection_sqli_data.h \
	libinjection_html5.h libinjection_html5.c \
	libinjection_xss.h libinjection_xss.c

libinjection_la_CPPFLAGS = -I$(top_srcdir)/src
libinjection_la_CFLAGS = -Werror

check_PROGRAMS = reader sqli testdriver testspeed testspeedxss

noinst_PROGRAMS = example1

reader_SOURCES = reader.c
reader_CPPFLAGS = -I$(top_srcdir)/src
reader_LDADD = libinjection.la
reader_CFLAGS = -Werror

sqli_SOURCES = sqli_cli.c
sqli_CPPFLAGS = -I$(top_srcdir)/src
sqli_LDADD = libinjection.la
sqli_CFLAGS = -Werror

testdriver_SOURCES = testdriver.c
testdriver_CPPFLAGS = -I$(top_srcdir)/src
testdriver_LDADD = libinjection.la
testdriver_CFLAGS = -Werror

testspeed_SOURCES = test_speed.c
testspeed_CPPFLAGS = -I$(top_srcdir)/src
testspeed_LDADD = libinjection.la
testspeed_CFLAGS = -Werror

testspeedxss_SOURCES = test_speed_xss.c
testspeedxss_CPPFLAGS = -I$(top_srcdir)/src
testspeedxss_LDADD = libinjection.la
testspeedxss_CFLAGS = -Werror

example1_SOURCES = example1.c
example1_CPPFLAGS = -I$(top_srcdir)/src
example1_LDADD = libinjection.la
example1_CFLAGS = -Werror
