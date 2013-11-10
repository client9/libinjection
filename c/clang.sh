#!/bin/sh

#
# adjust as needed for your clang setup
#
make clean
export CC=clang
export CFLAGS="-g -O3 -Werror -Weverything -Wno-padded"
make -e test
