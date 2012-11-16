
CC=gcc
CFLAGS=-g -O3 -Wall -Wextra -Wshadow -Wpointer-arith -Wcast-qual -Wcast-align
INDENT=indent
# Apple over-rides
#   Trying to avoid using libtool
#
APPLE=$(shell uname -a | grep -c Darwin)
ifeq ($(APPLE),1)
	SONAME=dylib
	RT=
	INDENT=gnuindent
	SHARED=-dynamiclib -flat_namespace
endif

help:
	@echo ""
	@echo "note: there is no library-- it's just one file"
	@echo "      see one of the unit tests or 'reader' to see how to"
	@echo "      compile"
	@echo ""
	@echo "make test_unit"
	@echo "make test_speed"
	@echo "make test_negative -- test false positives"
	@echo "make test_positive -- test sqli"
	@echo "make indent -- re-idents main c file"
	@echo "make unused -- print unused fingerprints"
	@echo "make sort -- resort fingerprints"
	@echo "make clean  -- cleanup"
	@echo "make lcov -- lcov"
	@echo "make reader -- line by line analyzer"
	@echo "make http -- runs mini-http server, handy for viewing lcov"
	@echo ""

reader: Makefile reader.c sqlparse_data.h sqlparse.h sqlparse.c modp_xml.c sqli_normalize.c sqli_fingerprints.h
	${CC}  ${CFLAGS} -o reader sqlparse.c reader.c sqli_normalize.c modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c

extractor: Makefile extractor.cpp sqlparse.c sqlparse.h sqli_normalize.h sqli_normalize.c sqlparse_data.h modp_xml.c sqli_fingerprints.h sqlparse_data.h
	g++ ${STATIC} ${CFLAGS} -o extractor extractor.cpp sqlparse.c sqli_normalize.c modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c

is_sqli: Makefile is_sqli_cli.cpp sqlparse.c sqlparse.h sqlparse_data.h modp_xml.c sqli_normalize.c  sqli_fingerprints.h sqlparse_data.h
	${CC}  ${CFLAGS} -O3 -o is_sqli is_sqli_cli.cpp sqlparse.c sqli_normalize.c  modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c

sqli: Makefile sqli_cli.c sqlparse.c sqlparse.h sqlparse_data.h  sqli_fingerprints.h
	${CC} ${CFLAGS} -o sqli sqli_cli.c sqlparse.c modp_ascii.c


test_speed: sqlparse_data.h sqlparse.c sqlparse.h test_speed.c
	${CC} ${CFLAGS} -o test_speed sqlparse.c test_speed.c  modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c
	./test_speed

test_unit: test_driver.py sqli sqlparse_data.h sqlparse.c sqlparse.h
	./test_driver.py ../tests/test-*.txt

valgrind: test_driver.py sqli sqlparse_data.h sqlparse.c sqlparse.h
	./test_driver.py --valgrind ../tests/test-*.txt

unused:
	-${MAKE} test_positive | grep True | awk '{print $$4}' | sort -u > /tmp/junk
	diff /tmp/junk fingerprints.txt  | grep '>'


# fail if any input is 'safe', e.g. not SQLi
test_positive: reader
	./reader ../data/sqli-*.txt

# invert... fail if any are sqli
test_negative: reader
	./reader -i ../data/false_*.txt

.PHONY: test_positive test_negative test test_unit test_speed

sqli_fingerprints.h: fingerprints.txt fingerprints2c.py
	./fingerprints2c.py > ./sqli_fingerprints.h

sqlparse_data.h: sqlparse_map.py sqlparse2c.py
	./sqlparse2c.py > ./sqlparse_data.h

indent: sqlparse.h sqlparse.c
	${INDENT} -kr -nut sqlparse.h sqlparse.c test_speed.c sqli_normalize.c reader.c
.PHONY: indent

sort:
	wc -l fingerprints.txt
	LC_ALL=C sort -u fingerprints.txt > /tmp/junk
	mv /tmp/junk fingerprints.txt
	wc -l fingerprints.txt

clean:
	rm -f *~ *.pyc
	rm -f test_tokens test_speed
	rm -rf *.dSYM
	rm -rf *.gcno *.gcda *.info
	rm -rf lcov-html
	rm -rf core* a.out
	rm -f reader extractor is_sqli lcov-reader sqli

lcov:
	g++ -g -fprofile-arcs -ftest-coverage -O0 -o sqli sqli_cli.cpp sqlparse.c modp_burl.c modp_ascii.c modp_xml.c
	lcov -b . --directory . --zerocounters
	./test_driver.py ../tests/test-*.txt
	lcov -b . --directory . --capture --output-file libinjection.info
	lcov -b . --directory . --remove libinjection.info '/usr/include*' -o libinjection.info
	lcov -b . --directory . --remove libinjection.info 'modp_*' -o libinjection.info
	lcov -b . --directory . --remove libinjection.info 'sqli' -o libinjection.info
	rm -rf lcov-html
	mkdir lcov-html
	genhtml -o lcov-html libinjection.info
.PHONY: lcov


lcov-reader: Makefile sqlparse_data.h sqlparse.h sqlparse.c reader.c sqli_normalize.c modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c
	g++ -g -O0 -fprofile-arcs -ftest-coverage -Wall -Wextra -o reader sqlparse.c reader.c sqli_normalize.c modp_qsiter.c modp_burl.c modp_ascii.c modp_xml.c
	lcov -b . --directory . --zerocounters
	-./reader ../data/*.txt
	lcov -b . --directory . --capture --output-file libinjection.info
	lcov -b . --directory . --remove libinjection.info '/usr/include*' -o libinjection.info
	lcov -b . --directory . --remove libinjection.info 'modp_*' -o libinjection.info
	lcov -b . --directory . --remove libinjection.info 'reader' -o libinjection.info
	rm -rf lcov-html
	mkdir lcov-html
	genhtml -o lcov-html libinjection.info
.PHONY: lcov-reader

http:
	python -m  SimpleHTTPServer
.PHONY: http
