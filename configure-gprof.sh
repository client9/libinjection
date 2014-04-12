#!/bin/sh
set -e
#
# gprof build
#
export CFLAGS="-O2 -pg -ansi"
./configure --with-pic
make clean
