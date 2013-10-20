
all:site

PAGES = \
	doc-sqli-false-negative.html \
	doc-sqli-false-positive.html \
	doc-sqli-references.html \
	doc-xss-references.html \
	doc-libinjection-references.html \
	doc-sqli-python.html \
	doc-sqli-php.html \
	doc.html \
	home.html
%.html: %.md base.html
	echo $<
	./mdgen.sh $< > $@

clean:
	rm -f ${PAGES}

site: Makefile ${PAGES}

.PHONY: site
