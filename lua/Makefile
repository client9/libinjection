
# either works

#LUA_INC_DIR=/opt/local/include/luajit-2.0
#LUA_LIB_DIR=/opt/local/lib
#LUA_LIB=luajit-5.1.2
#LUA=luajit

LUA_INC_DIR=/opt/local/include
LUA_LIB_DIR=/opt/local/lib
LUA_LIB=lua
LUA=lua

# need to hack a linux version here
#
# MAC OS X: note using ".so" suffix NOT ".dylib"
shared: libinjection_wrap.c
	gcc -g -O0 -I. -I${LUA_INC_DIR} -L${LUA_LIB_DIR} -l${LUA_LIB} \
	-dynamiclib libinjection_wrap.c libinjection_sqli.c -o libinjection.so

# build and run unit tests
# Uses a python helper to read the test files to generate
# a TAP test plan.  Easier that writing lots of LUA glue code
# and super-fast!
#
test-unit:
	./make_test.py > unit-test.t
	LUA_PATH='?.lua;lua-TestMore/src/?.lua' ${LUA} unit-test.t

libinjection_wrap.c: copy
	swig -lua libinjection.i

swig: copy libinjection_wrap.c

# not very efficient
copy:
	(cd ../c && make sort)
	cp ../c/libinjection.h .
	cp ../c/libinjection_sqli.c .
	cp ../c/libinjection_sqli_data.h .
	./generate_lua_fingerprints.py < ../c/sqlparse_data.json > sqlifingerprints.lua
.PHONY: copy

clean:
	rm -f *~
	rm -rf *.dSYM *.so *.dylib
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f lua libinjection_wrap.c sqlifingerprints.lua
	rm -f unit-test.t
