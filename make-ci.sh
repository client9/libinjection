#!/bin/sh

# this is the script that runs in CI

DASH=----------------------
echo $DASH
gcc --version
echo $DASH
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
(cd src; make analyze)

echo
echo "Done!"
