#!/bin/sh

#
# adjust as needed for your clang setup
#
make clean
export CC=clang
export CFLAGS="-g -O3 -Weverything -Wno-padded -L/usr/lib/gcc/x86_64-amazon-linux/4.7.2/"
COMPILER_PATH=/usr/lib/gcc/x86_64-amazon-linux/4.7.2/ make -e test
