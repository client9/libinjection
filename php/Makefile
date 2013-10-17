#
# this requires swig, and an installation of php (and php-dev tools)
#
# everything is copied and generating int the build directory
#
# I had to do gross hacks to make mac os x, phpunit / homebrew
#  combinations work
# MAC OS X - brew install phpunit

PHPUNIT=phpunit
APPLE=$(shell uname -a | grep -c Darwin)
ifeq ($(APPLE),1)
	PHPUNIT=./phpunit-homebrew.sh
endif

all: php

php: build build/libinjection.h build/libinjection_sqli.c build/libinjection_sqli_data.h build/config.m4 build/libinjection.i build/config.m4
	(cd build; swig -noproxy -php -Wextra libinjection.i)
	(cd build; phpize; ./configure ; make; make install)

words.php: Makefile json2php.py ../c/sqlparse_data.json
	./json2php.py < ../c/sqlparse_data.json > words.php

test-unit: php
	${PHPUNIT} testdriver.php

test: test-unit
.PHONY: test

build:
	mkdir build

build/libinjection.h: ../c/libinjection.h
	cp ../c/libinjection.h build/libinjection.h

build/libinjection_sqli.c: ../c/libinjection_sqli.c
	cp ../c/libinjection_sqli.c build/libinjection_sqli.c

build/libinjection_sqli_data.h: ../c/libinjection_sqli_data.h
	cp ../c/libinjection_sqli_data.h build/libinjection_sqli_data.h

build/libinjection.i: libinjection.i
	cp libinjection.i build/

build/config.m4: build config.m4
	cp config.m4 build/config.m4

clean:
	rm -f *~ *.o *.so
	rm -f words.php
	rm -rf build
