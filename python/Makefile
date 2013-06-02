
python: copy
	rm -f libinjection.py libinjection.pyc libinjection/libinjection_wrap.c
	python setup.py --verbose build --force
	sudo python setup.py --verbose install

test-unit: copy
	python setup.py build_ext --inplace
	PYTHON_PATH='.' nosetests -v test_driver.py

test: test-unit
.PHONY: test

# not very efficient
copy:
	(cd ../c && make sort)
	cp ../c/libinjection.h libinjection/.
	cp ../c/libinjection_sqli.c libinjection/.
	cp ../c/libinjection_sqli_data.h libinjection/.
.PHONY: copy

clean:
	rm -rf build dist
	rm -f *.pyc *~ _libinjection.so
	(cd libinjection; rm -f *.pyc *~)
	(cd libinjection; rm -f libinjection_wrap.c  libinjection.py)
	(cd libinjection; rm -f libinjection.h libinjection_sqli.c libinjection_sqli_data.h)

