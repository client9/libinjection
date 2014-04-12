#!/bin/sh
set -e
#
# gprof build
#
export CFLAGS="-g -O0 -fprofile-arcs -ftest-coverage -Wall -Wextra"
./configure --with-pic
make clean
