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

echo $DASH
echo "GCC + VALGRIND"
make clean
export CFLAGS="-Wall -Wextra -Werror -pedantic -ansi -g -O1"
export VALGRIND="valgrind --gen-suppressions=no --leak-check=full --show-leak-kinds=all --read-var-info=yes --error-exitcode=1 --track-origins=yes --suppressions=/build/src/alpine.supp"
make -e check
unset VALGRIND
unset CFLAGS
echo

echo
echo "Done!"
