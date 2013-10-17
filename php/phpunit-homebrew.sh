#!/bin/bash

# Mac OS X homebrew of phpunit is actually a bash
# script that calls into a phar file.
#
# This eliminates the possibility of dynamically
# loading modules or loading different init files since
# php is already started.
#
# This gross hack works around it.
#
VERSION=`phpunit --version | head -1 | awk '{print $2}'`

/usr/bin/env php \
    -d extension_dir=build/modules -d extension=libinjection.so \
    -d allow_url_fopen=On -d detect_unicode=Off /usr/local/Cellar/phpunit/${VERSION}/libexec/phpunit-${VERSION}.phar $*
