
CC=cc
LD=ld
CFLAGS=-Wall -Werror -ansi -g -O3
AR=libtool -static

LIBNAME=injection
STATICLIB_SUFFIX=a
STATICLIB=lib${LIBNAME}.${STATICLIB_SUFFIX}

SHAREDLIB_SUFFIX=so
SHAREDLIB=lib${LIBNAME}.${SHAREDLIB_SUFFIX}

HEADERS=libinjection_sqli_data.h libinjection_html5.h libinjection_xss.h

SOURCES=libinjection_sqli.c \
	libinjection_html5.c \
	libinjection_xss.c

OBJECTS=libinjection_sqli.o \
	libinjection_html5.o \
	libinjection_xss.o

EXES=reader testdriver testspeedxss testspeedsqli html5 sqli

all: ${SHAREDLIB} ${STATICLIB}

libinjection_sqli.o: libinjection_sqli.c
	${CC} ${CFLAGS} -c -o libinjection_sqli.o libinjection_sqli.c

libinjection_xss.o: libinjection_xss.c
	${CC} ${CFLAGS} -c -o libinjection_xss.o libinjection_xss.c

libinjection_html5.o: libinjection_html5.c
	${CC} ${CFLAGS} -c -o libinjection_html5.o libinjection_html5.c

${SHAREDLIB}: ${OBJECTS}
	${LD} -dylib -o ${SHAREDLIB} ${OBJECTS} -lc

${STATICLIB}: ${OBJECTS}
	rm -f ${STATICLIB}
	${AR} -o ${STATICLIB} ${OBJECTS}

samples: html5 sqli

.PHONY: samples

check: reader testdriver testspeedxss testspeedsqli
	@./test-driver.sh test-unit.sh
	@./test-driver.sh test-samples-sqli-negative.sh
	@./test-driver.sh test-samples-sqli-positive.sh
	@./test-driver.sh test-samples-xss-positive.sh
	@./test-driver.sh test-speed-xss.sh
	@./test-driver.sh test-speed-sqli.sh

test: check
.PHONY: check test

reader: reader.c ${STATICLIB}
	${CC} -o reader reader.c -L. ${STATICLIB}

sqli: sqli_cli.c ${STATICLIB}
	${CC} -o sqli sqli_cli.c -L. ${STATICLIB}

html5: html5_cli.c
	${CC} -o html5 html5_sqli.c ${STATICLIB}

testdriver: testdriver.c ${STATICLIB}
	${CC} -o testdriver testdriver.c -L. ${STATICLIB}

testspeedsqli: test_speed.c ${STATICLIB}
	${CC} -o testspeedsqli test_speed.c -L. ${STATICLIB}

testspeedxss: test_speed_xss.c ${STATICLIB}
	${CC} -o testspeedxss test_speed_xss.c -L. ${STATICLIB}

clean:
	rm -f *.so *.a *.o *.dylib *.lo
	rm -f *~
	rm -f *.log
	rm -f ${EXES}
