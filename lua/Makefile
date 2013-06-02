
#LUA_INC_DIR=/opt/local/include/luajit-2.0
#LUA_LIB_DIR=/opt/local/lib
#LUA_LIB=luajit-5.1

LUA_INC_DIR=/opt/local/include
LUA_LIB_DIR=/opt/local/lib
LUA_LIB=lua

lua: lua.c libinjection_wrap.c
	gcc -g -O0 -I. -I${LUA_INC_DIR} -L${LUA_LIB_DIR} -o lua \
		lua.c libinjection_wrap.c libinjection_sqli.c -l${LUA_LIB}

test-unit: lua
	./lua luatest.lua

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
	rm -rf *.dSYM
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f lua libinjection_wrap.c sqlifingerprints.lua

