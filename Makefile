
all:
	(cd c; ${MAKE} allbin; ${MAKE} test_unit)
	(cd python; ${MAKE} test)
	(cd lua; ${MAKE} test-unit)

clean:
	(cd c; ${MAKE} clean)
	(cd python; ${MAKE} clean)
	(cd lua; ${MAKE} clean)

.PHONY: clean
