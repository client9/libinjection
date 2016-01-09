
SUBDIRS=src

all:
	(cd src; ${MAKE} all)
check:
	(cd src; ${MAKE} check)
clean:
	(cd src; ${MAKE} clean)

.PHONY: all check clean


docker-console:
	docker run --rm -it -v $(PWD):/build -w /build nickg/libinjection-docker sh
