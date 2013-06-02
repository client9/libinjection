
lua: lua.c libinjection_wrap.c
	gcc -I. -I/usr/local/include -L/usr/local/lib lua.c libinjection_wrap.c libinjection_sqli.c -llua -o lua
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
	rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h
	rm -f lua libinjection_wrap.c sqlifingerprints.lua

