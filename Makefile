

clean:
	(cd c; ${MAKE} clean)
	(cd python; ${MAKE} clean)
	(cd lua; ${MAKE} clean)

.PHONY: clean
