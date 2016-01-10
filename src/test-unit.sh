#!/bin/sh
set -e
cd ../tests
pwd

find . -name 'test*.txt' | xargs ${VALGRIND} -n 1 ../src/testdriver
