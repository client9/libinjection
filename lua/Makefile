
# either works

# ubuntu
LUA_FLAGS=-I/usr/include/lua5.1 -llua5.1
LUA=/usr/bin/lua5.1

# ubuntu libjit 2
LUA_FLAGS=-I/usr/include/luajit-2.0 -lluajit5.1
LUA=XXX
# where is luajit?

# MAC OS X - "port" luajit
LUA_FLAGS=-I/opt/local/include/luajit-2.0 -L/opt/local/lib -lluajit-5.1.2
LUA=luajit

# MAC OS X - "port" for lua
LUA_FLAGS=-I/opt/local/include -L/opt/local/lib/ -llua
LUA=lua


SHARED=-shared -Wl,-soname,libinjection.so
CFLAGS= -O0 -g -Wall -Werror -fPIC -fno-common
APPLE=$(shell uname -a | grep -c Darwin)
ifeq ($(APPLE),1)
	SHARED=-dynamiclib
endif

# need to hack a linux version here
#
# MAC OS X: note using ".so" suffix NOT ".dylib"
libinjection.so: copy libinjection_wrap.c
	${CC} ${CFLAGS} -I. ${LUA_FLAGS} \
	${SHARED} libinjection_wrap.c libinjection_sqli.c -o libinjection.so

# build and run unit tests
# Uses a python helper to read the test files to generate
# a TAP test plan.  Easier that writing lots of LUA glue code
# and super-fast!
#
test-unit: libinjection.so lua-TestMore
	./make_test.py > unit-test.t
	LUA_PATH='?.lua;lua-TestMore/src/?.lua' ${LUA} unit-test.t

libinjection_wrap.c: libinjection.i
	swig -lua libinjection.i

sqlifingerprints.lua: generate_lua_fingerprints.py ../c/sqlparse_data.json
	./generate_lua_fingerprints.py > sqlifingerprints.lua

libinjection.h: ../c/libinjection.h
	cp ../c/libinjection.h libinjection.h

libinjection_sqli.c: ../c/libinjection_sqli.c
	cp ../c/libinjection_sqli.c libinjection_sqli.c

libinjection_sqli_data.h: ../c/libinjection_sqli_data.h
	cp ../c/libinjection_sqli_data.h libinjection_sqli_data.h

copy: libinjection.h libinjection_sqli.c libinjection_sqli_data.h
.PHONY: copy

# --depth 1 -- get without history
lua-TestMore:
	git clone --depth 1 https://github.com/fperrad/lua-TestMore.git

clean:
	rm -f *~
	rm -rf *.dSYM *.so *.dylib
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f sqlifingerprints.lua
	rm -f unit-test.t
	rm -f libinjection_sqli.c.*
	rm -f junit*.xml
