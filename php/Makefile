
#
#
all: php

php: libinjection_wrap.c copy words.php
	gcc `php-config --includes` -fpic -c libinjection_wrap.c libinjection_sqli.c
	gcc -shared libinjection_sqli.o libinjection_wrap.o -o libinjection.so

#python: copy libinjection/libinjection_wrap.c
#	rm -f libinjection.py libinjection.pyc
#	python setup.py --verbose build --force
#	sudo python setup.py --verbose install

words.php: Makefile json2php.py ../c/sqlparse_data.json
	./json2php.py < ../c/sqlparse_data.json > words.php

test-unit: php
	phpunit -v testdriver.php

test: test-unit
.PHONY: test

speed:
	./speedtest.py

libinjection.h: ../c/libinjection.h
	cp ../c/libinjection.h libinjection.h

libinjection_sqli.c: ../c/libinjection_sqli.c
	cp ../c/libinjection_sqli.c libinjection_sqli.c

libinjection_sqli_data.h: ../c/libinjection_sqli_data.h
	cp ../c/libinjection_sqli_data.h libinjection_sqli_data.h

libinjection_wrap.c: libinjection.i libinjection.h
	swig -noproxy -php -Wextra libinjection.i

copy: libinjection.h libinjection_sqli.c libinjection_sqli_data.h

clean:
	rm -f *~ *.o *.so
	rm -f words.php
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f libinjection.php php_libinjection.h libinjection_wrap.c
