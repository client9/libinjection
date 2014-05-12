
SUBDIRS=src

all:
	(cd src; ${MAKE} all)
check:
	(cd src; ${MAKE} check)
clean:
	(cd src; ${MAKE} clean)

.PHONY: all check clean

