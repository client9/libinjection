
# either works

#LUA_INC_DIR=/opt/local/include/luajit-2.0
#LUA_LIB_DIR=/opt/local/lib
#LUA_LIB=luajit-5.1.2
#LUA=luajit

LUA_INC_DIR=/opt/local/include
LUA_LIB_DIR=/opt/local/lib
LUA_LIB=lua
LUA=lua

SHARED=-shared -Wl,-soname,libinjection.so
CFLAGS= -O0 -g -Wall -Werror
APPLE=$(shell uname -a | grep -c Darwin)
ifeq ($(APPLE),1)
	SHARED=-dynamiclib
endif

# need to hack a linux version here
#
# MAC OS X: note using ".so" suffix NOT ".dylib"
libinjection.so: libinjection_wrap.c
	${CC} ${CFLAGS} -I. -I${LUA_INC_DIR} -L${LUA_LIB_DIR} -l${LUA_LIB} \
	${SHARED} libinjection_wrap.c libinjection_sqli.c -o libinjection.so

# build and run unit tests
# Uses a python helper to read the test files to generate
# a TAP test plan.  Easier that writing lots of LUA glue code
# and super-fast!
#
test-unit: libinjection.so
	./make_test.py > unit-test.t
	LUA_PATH='?.lua;lua-TestMore/src/?.lua' ${LUA} unit-test.t

libinjection_wrap.c: copy libinjection.i
	swig -lua libinjection.i

fingerprints.lua: generate_lua_fingerprints.py ../c/sqlparse_data.json
	./generate_lua_fingerprints.py < ../c/sqlparse_data.json > sqlifingerprints.lua

libinjection.h: ../c/libinjection.h
	cp ../c/libinjection.h libinjection.h

libinjection_sqli.c: ../c/libinjection_sqli.c
	cp ../c/libinjection_sqli.c libinjection_sqli.c

libinjection_sqli_data.h: ../c/libinjection_sqli_data.h
	cp ../c/libinjection_sqli_data.h libinjection_sqli_data.h

copy: libinjection.h libinjection_sqli.c libinjection_sqli_data.h

clean:
	rm -f *~
	rm -rf *.dSYM *.so *.dylib
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f lua libinjection_wrap.c sqlifingerprints.lua
	rm -f unit-test.t
