#!/bin/sh
# this is the script that runs in CI
set -e

DASH=----------------------
echo $DASH
gcc --version
echo $DASH
make clean
make -e check
echo

echo $DASH
echo "GCC + VALGRIND"
export VALGRIND="libtool --mode=execute `which valgrind` --gen-suppressions=no --read-var-info=yes --error-exitcode=1 --track-origins=yes"
make -e check
echo

echo
echo $DASH
clang --version
echo $DASH
./configure-clang.sh

echo
echo $DASH
echo "CLANG STATIC ANALYZER"
echo
cd src
make analyze

echo
echo $DASH
cppcheck --version
echo

cppcheck --std=c89 \
         --enable=all \
         --inconclusive \
         --suppress=variableScope \
         --suppress=missingIncludeSystem \
         --quiet \
         --error-exitcode=1 \
         --template='{file}:{line} {id} {severity} {message}' \
         .
echo "passed"

echo
echo "Done!"
