
SUBDIRS=src

all:
	(cd src; ${MAKE} all)
check:
	(cd src; ${MAKE} check)
clean:
	@(cd src; ${MAKE} clean)

.PHONY: all check clean


docker-console:
	docker run --rm -it \
		-e COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN \
		-v $(PWD):/build \
		-w /build \
		nickg/libinjection-docker \
		sh

docker-ci:
	docker run --rm \
		-e COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN \
		-v $(PWD):/build \
		-w /build \
		nickg/libinjection-docker \
		./make-ci.sh
