
STATIC=-static
CFLAGS=-g -O3 -Wall -Wextra
INDENT=indent
# Apple over-rides
#   Trying to avoid using libtool
#
APPLE=$(shell uname -a | grep -c Darwin)
ifeq ($(APPLE),1)
	STATIC=
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
	@echo "make clean  -- cleanup"
	@echo "make lcov -- lcov"
	@echo "make reader -- line by line analyzer"
	@echo "make http -- runs mini-http server, handy for viewing lcov"
	@echo ""

reader: Makefile reader.cpp sqlparse_data.c sqlparse.h sqlparse.c
	g++ ${STATIC} ${CFLAGS} -o reader sqlparse.c reader.cpp -L/usr/local/lib -lmodpbase64

test_tokens.cpp: test_tokens.hpp
	../cxxtest/bin/cxxtestgen --error-printer -o test_tokens.cpp test_tokens.hpp

test_speed.cpp: test_speed.hpp
	../cxxtest/bin/cxxtestgen --error-printer -o test_speed.cpp test_speed.hpp

test_speed: sqlparse_data.c sqlparse.c sqlparse.h test_speed.cpp
	g++ -I../cxxtest ${CFLAGS} -o test_speed sqlparse.c test_speed.cpp
	./test_speed

test_unit: sqlparse_data.c sqlparse.c sqlparse.h test_tokens.cpp
	rm -f ./test_tokens
	g++ -I../cxxtest ${CFLAGS} -o test_tokens test_tokens.cpp sqlparse.c
	./test_tokens

# fail if any input is 'safe', e.g. not SQLi
test_positive: reader
	./reader ../data/sqli-*.txt

# invert... fail if any are sqli
test_negative: reader
	./reader -i ../data/false_*

.PHONY: test_positive test_negative test test_unit test_speed

sqlparse_data.h: sqlparse_map.py sqlparse2c.py fingerprints.txt
	./sqlparse2c.py > ./sqlparse_data.h

indent: sqlparse.h sqlparse.c
	${INDENT} -kr -nut sqlparse.h sqlparse.c
clean:
	rm -f *~ *.pyc
	rm -f test_tokens test_tokens.cpp test_speed.cpp reader test_speed
	rm -rf *.dSYM
	rm -rf *.gcno *.gcda
	rm -rf lcov-html
	rm -rf core* a.out
lcov:
	rm -f test_tokens
	../cxxtest/bin/cxxtestgen --error-printer -o test_tokens.cpp test_tokens.hpp
	g++ -g -fprofile-arcs -ftest-coverage -O0 -I../cxxtest -o test_tokens test_tokens.cpp sqlparse.c
	lcov -b . --directory . --zerocounters
	./test_tokens
	lcov -b . --directory . --capture --output-file stringencoders.info
	lcov -b . --directory . --remove stringencoders.info '/usr/include*' -o stringencoders.info
	lcov -b . --directory . --remove stringencoders.info 'cxxtest/*' -o stringencoders.info
	lcov -b . --directory . --remove stringencoders.info 'test_*' -o stringencoders.info
	rm -rf lcov-html
	mkdir lcov-html
	genhtml -o lcov-html stringencoders.info
.PHONY: lcov



lcov-reader: Makefile reader.cpp sqlparse_data.c sqlparse.h sqlparse.c
	g++ -g -O0 -fprofile-arcs -ftest-coverage -Wall -Wextra -o reader sqlparse.c reader.cpp -lmodpbase64
	lcov -b . --directory . --zerocounters
	./reader ../urls*.txt
	lcov -b . --directory . --capture --output-file stringencoders.info
	lcov -b . --directory . --remove stringencoders.info '/usr/include*' -o stringencoders.info
	lcov -b . --directory . --remove stringencoders.info 'cxxtest/*' -o stringencoders.info
	lcov -b . --directory . --remove stringencoders.info 'test_*' -o stringencoders.info
	rm -rf lcov-html
	mkdir lcov-html
	genhtml -o lcov-html stringencoders.info
.PHONY: lcov


http:
	python -m  SimpleHTTPServer
.PHONY: http
