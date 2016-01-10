#!/bin/sh
set -e
cd ../tests
pwd

find . -name 'test*.txt' | xargs -n 1 ${VALGRIND} ../src/testdriver
