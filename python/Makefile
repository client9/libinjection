
#
# SWIG libinjection.i -> libinjection_wrap.c
#  is done in 'setup.py'
#
python: copy
	rm -f libinjection.py libinjection.pyc libinjection/libinjection_wrap.c
	python setup.py --verbose build --force
	sudo python setup.py --verbose install

words.py: Makefile json2python.py ../c/sqlparse_data.json
	./json2python.py < ../c/sqlparse_data.json > words.py

test-unit: copy words.py
	python setup.py build_ext --inplace
	PYTHON_PATH='.' nosetests -v --with-xunit test_driver.py

test: test-unit
.PHONY: test

speed:
	./speedtest.py

libinjection/libinjection.h: ../c/libinjection.h
	cp ../c/libinjection.h libinjection/libinjection.h

libinjection/libinjection_sqli.c: ../c/libinjection_sqli.c
	cp ../c/libinjection_sqli.c libinjection/libinjection_sqli.c

libinjection/libinjection_sqli_data.h: ../c/libinjection_sqli_data.h
	cp ../c/libinjection_sqli_data.h libinjection/libinjection_sqli_data.h

copy: libinjection/libinjection.h libinjection/libinjection_sqli.c libinjection/libinjection_sqli_data.h

clean:
	rm -rf build dist
	rm -f *.pyc *~ _libinjection.so
	rm -f nosetests.xml
	(cd libinjection; rm -f *.pyc *~)
	(cd libinjection; rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h)

