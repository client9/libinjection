
all:site

PAGES = doc-sqli-false-negative.html doc-sqli-false-positive.html doc-sqli-references.html \
	doc-sqli-python.html doc.html

%.html: %.md base.html
	echo $<
	./mdgen.sh $< > $@


clean:
	rm -f ${PAGES}

site: Makefile ${PAGES}


.PHONY: site
